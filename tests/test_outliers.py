import numpy as np
import pandas as pd

from workshop import outliers as ol


def _s():
    return pd.Series(np.random.default_rng(0).normal(20, 4, 300))


def test_detect_flags_injected_outliers():
    s = ol.inject(_s(), n=6, seed=1)
    mask, lo, hi = ol.detect(s, "iqr")
    assert mask.sum() >= 5          # catches most of the injected extremes


def test_cap_reduces_max():
    s = ol.inject(_s(), n=6, seed=1)
    mask, lo, hi = ol.detect(s, "iqr")
    assert ol.cap(s, lo, hi).max() <= hi + 1e-9
    assert ol.cap(s, lo, hi).max() < s.max()


def test_remove_drops_flagged():
    s = ol.inject(_s(), n=6, seed=1)
    mask, lo, hi = ol.detect(s, "iqr")
    assert len(ol.remove(s, mask)) == len(s) - int(mask.sum())
