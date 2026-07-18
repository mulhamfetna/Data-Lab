from workshop import active


def test_curves_valid():
    for strat in ["random", "uncertainty"]:
        c = active.learning_curve(strat, seed=0)
        assert len(c) >= 10
        assert all(0.0 <= a <= 1.0 for a in c)


def test_uncertainty_learns_faster():
    r = active.learning_curve("random", seed=0)
    u = active.learning_curve("uncertainty", seed=0)
    # uncertainty reaches accuracy with fewer labels → larger area under the curve
    assert sum(u) >= sum(r)
