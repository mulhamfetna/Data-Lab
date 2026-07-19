import workshop.llm as llm

PROVIDER_ENVS = ["GROQ_API_KEY", "OPENROUTER_API_KEY", "HF_TOKEN",
                 "OLLAMA_HOST", "LLM_PROVIDER", "LLM_MODEL", "SPACE_ID"]


def _clear(monkeypatch):
    for e in PROVIDER_ENVS:
        monkeypatch.delenv(e, raising=False)


def test_offline_returns_no_live_answer(monkeypatch):
    _clear(monkeypatch)
    assert llm.has_provider() is False
    assert llm.active_provider() is None
    text, live = llm.complete("hello")
    assert text is None and live is False
    assert llm.provider_label() == "offline simulation"


def test_groq_key_activates_groq(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    assert llm.has_provider() is True
    assert llm.active_provider()[0] == "Groq"
    label = llm.provider_label()
    assert "Groq" in label and "live" in label


def test_openrouter_free_model_default(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-test")
    assert llm.active_provider()[0] == "OpenRouter"
    assert ":free" in llm.model_name()


def test_ollama_needs_host(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:11434")
    assert llm.active_provider()[0] == "Ollama"


def test_model_override(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    monkeypatch.setenv("LLM_MODEL", "custom-mini")
    assert llm.model_name() == "custom-mini"


def test_hf_default_model_is_open_and_cost_routed(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("HF_TOKEN", "hf-test")
    assert llm.active_provider()[0] == "Hugging Face"
    model = llm.model_name()
    # Verified as served by the HF router; must stay non-gated + cost-routed.
    assert model.startswith("openai/gpt-oss-20b")
    assert model.endswith(":cheapest")


def test_hf_space_prefers_hugging_face(monkeypatch):
    """On a Space, HF wins even when another provider is also configured."""
    _clear(monkeypatch)
    monkeypatch.setenv("SPACE_ID", "mulhamfetna/Data-Lab")
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    monkeypatch.setenv("HF_TOKEN", "hf-test")
    assert llm.on_hf_space() is True
    assert llm.active_provider()[0] == "Hugging Face"


def test_off_space_keeps_groq_first(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    monkeypatch.setenv("HF_TOKEN", "hf-test")
    assert llm.on_hf_space() is False
    assert llm.active_provider()[0] == "Groq"


def test_space_without_hf_token_falls_back(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("SPACE_ID", "mulhamfetna/Data-Lab")
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    assert llm.active_provider()[0] == "Groq"
