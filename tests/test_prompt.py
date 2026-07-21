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


def test_common_imperative_verbs_count_as_a_task():
    # Regression: the page's default example uses "Tell ..."; verbs like tell/reply/
    # apologise must register as stating the task, or the engineered prompt loses a point.
    for verb in ("tell", "reply to", "apologise to", "respond to", "answer", "describe"):
        s = pr.score_prompt(f"{verb} an unhappy customer about their late order")
        assert s["hits"]["task"], f"{verb!r} should count as a task"


def test_default_example_engineered_prompt_scores_full():
    # The exact default task shown on the Prompt playground page.
    task = "Tell an unhappy customer their late order is on the way"
    s = pr.score_prompt(pr.build_variants(task)["engineered"])
    assert s["score"] == s["max"] == len(pr.RUBRIC)


def test_label_for_returns_human_text():
    assert "role" in pr.label_for("persona").lower()
