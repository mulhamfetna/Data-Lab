from workshop import drift as d


def test_no_shift_is_stable():
    ref = d.reference()
    assert d.report(ref, d.live(0))["drifted"] is False


def test_large_shift_is_flagged():
    ref = d.reference()
    r = d.report(ref, d.live(20))
    assert r["drifted"] is True
    assert r["psi"] > 0.25
