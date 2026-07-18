import pytest

from workshop import zeroshot as zs


@pytest.fixture(autouse=True)
def _offline(monkeypatch):
    for e in ("GROQ_API_KEY", "OPENROUTER_API_KEY", "HF_TOKEN", "OLLAMA_HOST"):
        monkeypatch.delenv(e, raising=False)


def test_billing_ticket_routes_to_billing():
    r = zs.classify("I was charged twice, please refund the payment.")
    assert r["label"] == "Billing"
    assert r["is_live"] is False


def test_shipping_ticket_routes_to_shipping():
    assert zs.classify("my package is late and tracking never updated")["label"] == "Shipping"


def test_technical_ticket_routes_to_technical():
    assert zs.classify("the app crashes and I can't log in with my password")["label"] == "Technical"


def test_scores_cover_all_labels():
    r = zs.classify("refund my payment")
    assert set(r["scores"]) == set(zs.LABELS)
    assert r["scores"]["Billing"] >= 1
