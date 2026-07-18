from workshop import tokenize as tk


def test_word_tokens_split_punctuation():
    toks = tk.word_tokens("Nour Store sells coffee, tea!")
    assert "coffee" in toks and "," in toks and "!" in toks
    assert "coffee," not in toks


def test_stats_shapes():
    s = tk.stats("hello world")
    assert s["words"] == 2
    assert s["characters"] == 11
    assert s["est_llm_tokens"] >= 1


def test_estimate_scales_with_length():
    assert tk.estimate_llm_tokens("a" * 40) > tk.estimate_llm_tokens("a" * 4)
