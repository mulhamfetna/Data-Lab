from workshop import summarize as sm

TEXT = ("Revenue rose sharply this quarter. Coffee was the top category. Coffee sales grew "
        "because of fresh roasting. The weather was cold on Tuesday. International shipping is "
        "the biggest future opportunity for coffee revenue.")


def test_split_sentences_counts():
    assert len(sm.split_sentences(TEXT)) == 5


def test_extractive_summary_is_shorter_and_ordered():
    summary = sm.extractive_summary(TEXT, 2)
    assert len(summary) == 2
    idx = [TEXT.index(s) for s in summary]
    assert idx == sorted(idx)                       # original document order preserved


def test_extractive_favours_high_signal_sentences():
    summary = " ".join(sm.extractive_summary(TEXT, 2))
    assert "coffee" in summary.lower()              # the recurring theme
    assert "Tuesday" not in summary                 # the off-topic filler is dropped


def test_compression_between_zero_and_one():
    c = sm.compression(TEXT, sm.extractive_summary(TEXT, 2)[0])
    assert 0 < c < 1


def test_summarize_offline_is_extractive(monkeypatch):
    for e in ("GROQ_API_KEY", "OPENROUTER_API_KEY", "HF_TOKEN", "OLLAMA_HOST"):
        monkeypatch.delenv(e, raising=False)
    r = sm.summarize(TEXT, 2)
    assert r["is_live"] is False and r["method"] == "extractive"
    assert r["compression"] < 1
