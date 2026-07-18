from workshop import prompt as pr


def test_variants_increase_in_richness():
    v = pr.build_variants("summarize the customer feedback")
    assert set(v) == {"vague", "specific", "formatted", "engineered"}
    scores = {k: pr.score_prompt(t)["score"] for k, t in v.items()}
    assert scores["engineered"] > scores["vague"]


def test_engineered_prompt_hits_every_rubric_element():
    s = pr.score_prompt(pr.build_variants("classify this ticket")["engineered"])
    assert s["score"] == s["max"] == len(pr.RUBRIC)


def test_vague_prompt_is_weak():
    assert pr.score_prompt("write a poem")["score"] <= 2


def test_label_for_returns_human_text():
    assert "role" in pr.label_for("persona").lower()
