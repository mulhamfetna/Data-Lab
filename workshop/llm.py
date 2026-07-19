"""Unified LLM access for the GenAI demos — free / lightweight providers only.

The workshop must run cheaply and offline-safe, so every GenAI demo has TWO paths:

* **Live** — when a provider is configured, ``complete()`` calls a small, free model
  through that provider's OpenAI-compatible chat endpoint and returns a real answer.
* **Offline** — with nothing configured, ``complete()`` returns ``(None, False)`` and
  each demo falls back to its own deterministic, clearly-labeled simulation.

Supported providers (all free tiers, all lightweight demo-grade models, all reached
through the same ``/chat/completions`` shape):

* **Groq** — ``GROQ_API_KEY``           (default ``llama-3.1-8b-instant``)
* **OpenRouter** — ``OPENROUTER_API_KEY`` (default ``meta-llama/llama-3.2-3b-instruct:free``)
* **Hugging Face** — ``HF_TOKEN``        (default ``meta-llama/Llama-3.2-3B-Instruct``)
* **Ollama** — local, keyless; set ``OLLAMA_HOST`` to enable (default ``llama3.2:1b``)

Override the picked model with ``LLM_MODEL`` and force a provider with ``LLM_PROVIDER``.
We never dress a simulation up as a real model — ``provider_label()`` is shown in the UI
so the audience always knows which path produced the text on screen.
"""
from __future__ import annotations

import os

# name, env-var holding the API key (None = keyless), base URL, default light free model
PROVIDERS: list[tuple[str, str | None, str, str]] = [
    ("Groq", "GROQ_API_KEY", "https://api.groq.com/openai/v1", "llama-3.1-8b-instant"),
    ("OpenRouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",
     "meta-llama/llama-3.2-3b-instruct:free"),
    # Model id verified against https://router.huggingface.co/v1/models: open-weights
    # (no license gating), served by ~8 providers, and ":cheapest" routes to the lowest
    # price per output token to stretch the free monthly quota.
    ("Hugging Face", "HF_TOKEN", "https://router.huggingface.co/v1",
     "openai/gpt-oss-20b:cheapest"),
    ("Ollama", None, "__ollama__", "llama3.2:1b"),
]


def _ollama_base() -> str:
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/") + "/v1"


def on_hf_space() -> bool:
    """True when running inside a Hugging Face Space (HF sets SPACE_ID)."""
    return bool(os.environ.get("SPACE_ID"))


def _provider_order() -> list[tuple[str, str | None, str, str]]:
    """Provider preference. On a Hugging Face Space, prefer HF's own inference router."""
    order = list(PROVIDERS)
    if on_hf_space():
        order.sort(key=lambda p: 0 if p[0] == "Hugging Face" else 1)
    return order


def active_provider() -> tuple[str, str | None, str, str] | None:
    """The first configured provider, or None when nothing is set up (offline)."""
    forced = os.environ.get("LLM_PROVIDER", "").strip().lower()
    for name, key_env, base, model in _provider_order():
        base = _ollama_base() if base == "__ollama__" else base
        enabled = (bool(key_env) and bool(os.environ.get(key_env))) or \
                  (key_env is None and bool(os.environ.get("OLLAMA_HOST")))
        if forced:
            if name.lower().startswith(forced):
                return (name, key_env, base, model)
        elif enabled:
            return (name, key_env, base, model)
    return None


def has_provider() -> bool:
    """True when a real model call is possible."""
    return active_provider() is not None


def model_name() -> str | None:
    prov = active_provider()
    if not prov:
        return None
    return os.environ.get("LLM_MODEL", prov[3])


def provider_label() -> str:
    prov = active_provider()
    if not prov:
        return "offline simulation"
    return f"{prov[0]} · {model_name()} · live"


def complete(prompt: str, system: str | None = None,
             max_tokens: int = 512, temperature: float = 0.3):
    """Return ``(text, is_live)``.

    When a provider is configured, POST to its OpenAI-compatible ``/chat/completions``
    and return ``(answer, True)``. Otherwise return ``(None, False)`` so the caller uses
    its own offline fallback. Deliberately thin — the teaching logic lives in each demo's
    own pure module, not here.
    """
    prov = active_provider()
    if not prov:
        return None, False
    import requests  # already a dependency; imported lazily to keep offline import cheap

    _name, key_env, base, _default = prov
    headers = {"Content-Type": "application/json"}
    if key_env and os.environ.get(key_env):
        headers["Authorization"] = f"Bearer {os.environ[key_env]}"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model_name(), "messages": messages,
               "max_tokens": max_tokens, "temperature": temperature}
    resp = requests.post(f"{base}/chat/completions", json=payload,
                         headers=headers, timeout=30)
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"]
    return text.strip(), True
