import numpy as np
import pandas as pd

from workshop import synth


def _real(seed=0, n=300):
    rng = np.random.default_rng(seed)
    age = rng.normal(40, 10, n)
    income = age * 100 + rng.normal(0, 500, n)   # correlated with age
    return pd.DataFrame({"age": age, "income": income})


def test_generate_shape_and_columns():
    real = _real()
    syn = synth.generate(real, n=500, seed=1)
    assert len(syn) == 500
    assert list(syn.columns) == list(real.columns)


def test_utility_means_close():
    real = _real()
    syn = synth.generate(real, n=2000, seed=1)
    rep = synth.utility_report(real, syn)
    for col in real.columns:
        assert abs(rep[col]["synth_mean"] - rep[col]["real_mean"]) < 0.15 * abs(rep[col]["real_mean"])


def test_utility_preserves_correlation():
    real = _real()
    syn = synth.generate(real, n=2000, seed=1)
    rep = synth.utility_report(real, syn)
    assert rep["corr_abs_diff"] < 0.15


def test_privacy_no_exact_copies():
    real = _real()
    syn = synth.generate(real, n=500, seed=1)
    rep = synth.privacy_report(real, syn)
    assert rep["exact_match_frac"] == 0.0
    assert rep["min_distance"] > 0
