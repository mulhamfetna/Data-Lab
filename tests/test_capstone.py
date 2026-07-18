from workshop import capstone as cap


def test_all_correct_scores_full():
    answers = {i: s["best"] for i, s in enumerate(cap.STEPS)}
    r = cap.grade(answers)
    assert r["score"] == r["max"] == len(cap.STEPS)
    assert all(x["correct"] for x in r["results"])


def test_all_wrong_scores_zero():
    answers = {i: (s["best"] + 1) % len(s["options"]) for i, s in enumerate(cap.STEPS)}
    assert cap.grade(answers)["score"] == 0


def test_partial_and_missing_answers():
    answers = {0: cap.STEPS[0]["best"]}          # only first answered
    r = cap.grade(answers)
    assert r["score"] == 1
    assert r["results"][1]["correct"] is False   # unanswered counts as wrong


def test_verdict_tiers():
    assert "fluent" in cap.verdict(5, 5).lower()
    assert cap.verdict(3, 5) != cap.verdict(5, 5)
    assert cap.verdict(0, 5) != cap.verdict(5, 5)


def test_steps_are_well_formed():
    for s in cap.STEPS:
        assert 0 <= s["best"] < len(s["options"])
        assert s["stage"] and s["why"]
