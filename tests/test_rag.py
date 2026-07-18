from workshop import rag


def test_retrieve_ranks_relevant_snippet_first():
    top = rag.retrieve("how do I get a refund?", k=1)[0]
    assert "refund" in top[0].lower()
    assert top[1] > 0


def test_answer_is_grounded_for_known_question(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    r = rag.answer("how long does delivery take?")
    assert r["grounded"] is True
    assert r["is_live"] is False               # offline extractive path
    assert "delivery" in r["answer"].lower() or "business days" in r["answer"].lower()


def test_answer_refuses_out_of_scope_question():
    r = rag.answer("what is the capital of France?")
    assert r["grounded"] is False
    assert "don't have" in r["answer"].lower()


def test_retrieve_respects_k():
    assert len(rag.retrieve("delivery", k=3)) == 3
