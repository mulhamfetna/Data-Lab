import os

from workshop import ui


def test_load_secrets_is_noop_without_store(monkeypatch):
    # No secrets file locally — the bridge must never raise and must not invent keys.
    for k in ui._SECRET_KEYS:
        monkeypatch.delenv(k, raising=False)
    ui.load_secrets_to_env()
    assert "GROQ_API_KEY" not in os.environ


def test_existing_env_is_not_overwritten(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "already-set")
    ui.load_secrets_to_env()
    assert os.environ["GROQ_API_KEY"] == "already-set"
