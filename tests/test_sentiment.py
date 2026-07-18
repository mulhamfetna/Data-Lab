from workshop import sentiment as se


def test_scoring_direction():
    assert se.score("great fast friendly") > 0
    assert se.score("slow bad damaged") < 0


def test_labels():
    assert se.label("amazing quick service") == "positive"
    assert se.label("rude and late") == "negative"


def test_summarize_counts():
    out = se.summarize(["great service", "slow and bad", "quick delivery"])
    assert out.get("positive", 0) >= 2 and out.get("negative", 0) >= 1
