from workshop import guardrails as gr


def test_grounded_answer_scores_high():
    rep = gr.grounding_report(gr.GROUNDED_ANSWER, gr.SOURCE)
    assert rep["grounded_fraction"] == 1.0


def test_hallucinated_answer_scores_lower():
    rep = gr.grounding_report(gr.HALLUCINATED_ANSWER, gr.SOURCE)
    assert rep["grounded_fraction"] < 1.0


def test_sentence_support_detects_invented_fact():
    # A claim with no basis in the source has low support.
    s = "Nour Store offers free international shipping to every country."
    assert gr.sentence_support(s, gr.SOURCE) < 0.6


def test_supported_sentence_has_high_support():
    s = "Refunds are within 14 days of delivery."
    assert gr.sentence_support(s, gr.SOURCE) >= 0.6


def test_report_marks_each_sentence():
    rep = gr.grounding_report(gr.HALLUCINATED_ANSWER, gr.SOURCE)
    assert all("supported" in r and "support" in r for r in rep["sentences"])
    assert any(not r["supported"] for r in rep["sentences"])
