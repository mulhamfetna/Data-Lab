from workshop import stats_traps as st_


def test_ci_narrows_with_more_data():
    assert st_.ci_width(1000) < st_.ci_width(50)


def test_p_hacking_finds_false_positives_near_5pct():
    r = st_.p_hacking(300, seed=0)
    assert 0.01 <= r["rate"] <= 0.12          # ~5% by construction (all groups identical)
    assert r["false_positives"] > 0
