import numpy as np
import pandas as pd

from workshop import scaling as sc


def _s():
    return pd.Series(np.random.default_rng(0).normal(500, 120, 300))


def test_minmax_in_unit_range():
    out = sc.minmax(_s())
    assert abs(out.min()) < 1e-9 and abs(out.max() - 1) < 1e-9


def test_zscore_standardized():
    out = sc.zscore(_s())
    assert abs(out.mean()) < 1e-6
    assert abs(out.std() - 1) < 1e-6
