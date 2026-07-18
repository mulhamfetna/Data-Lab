from workshop import weak


def test_labeling_functions_vote():
    assert weak.lf_positive("great fast service") == 1
    assert weak.lf_negative("slow and damaged") == -1
    assert weak.lf_positive("a neutral sentence") == 0


def test_majority_vote():
    assert weak.majority_vote([1, 0]) == 1
    assert weak.majority_vote([0, -1]) == 0
    assert weak.majority_vote([0, 0]) is None


def test_evaluate_covers_and_is_accurate():
    r = weak.evaluate()
    assert r["coverage"] >= 0.7
    assert r["accuracy"] >= 0.8
