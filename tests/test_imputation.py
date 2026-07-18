import numpy as np
import pandas as pd

from workshop import imputation as im


def _s():
    return pd.Series(np.arange(1, 101, dtype=float))


def test_with_missing_creates_gaps():
    s = im.with_missing(_s(), frac=0.2, seed=1)
    assert s.isna().sum() == 20


def test_mean_impute_fills_all_and_keeps_count():
    s = im.with_missing(_s(), seed=1)
    out = im.impute(s, "mean")
    assert out.isna().sum() == 0
    assert len(out) == len(s)


def test_drop_reduces_count():
    s = im.with_missing(_s(), seed=1)
    assert len(im.impute(s, "drop")) < len(s)


def test_zero_lowers_mean():
    s = im.with_missing(_s(), seed=1)
    assert im.impute(s, "zero").mean() < im.impute(s, "mean").mean()
