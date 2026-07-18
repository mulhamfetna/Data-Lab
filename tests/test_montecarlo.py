import numpy as np

from workshop import montecarlo as mc


def test_simulate_is_deterministic_with_seed():
    a = mc.simulate(n=2000, seed=1)
    b = mc.simulate(n=2000, seed=1)
    assert np.array_equal(a, b)
    assert a.size == 2000


def test_summary_orders_percentiles():
    s = mc.summary(mc.simulate(n=10_000, seed=7))
    assert s["p5"] < s["mean"] < s["p95"]
    assert 0.0 <= s["prob_loss"] <= 1.0


def test_more_uncertainty_raises_loss_probability():
    low = mc.summary(mc.simulate(n=10_000, seed=3, units_sd=30, margin_sd=0.3))
    high = mc.summary(mc.simulate(n=10_000, seed=3, units_sd=250, margin_sd=3.0))
    assert high["prob_loss"] >= low["prob_loss"]


def test_histogram_bins_sum_to_n():
    outcomes = mc.simulate(n=5000, seed=2)
    _centers, counts = mc.histogram(outcomes, bins=30)
    assert counts.sum() == 5000
