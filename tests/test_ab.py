from workshop import ab


def test_large_difference_is_significant():
    r = ab.analyze(1000, 100, 1000, 150)
    assert r["significant"] is True
    assert r["rate_b"] > r["rate_a"] and r["lift"] > 0


def test_tiny_difference_not_significant():
    assert ab.analyze(1000, 100, 1000, 104)["significant"] is False


def test_simulate_returns_counts():
    ca, cb = ab.simulate(500, 0.1, 0.2, seed=1)
    assert 0 <= ca <= 500 and 0 <= cb <= 500
