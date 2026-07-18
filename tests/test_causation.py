from workshop import causation as ca


def test_spurious_correlation_and_confounder():
    c = ca.correlations(ca.data())
    assert c["ice_cream_vs_drownings"] > 0.5          # strong (but spurious) link
    assert c["temp_vs_ice_cream"] > 0.5               # the real cause of each
    assert c["temp_vs_drownings"] > 0.5
