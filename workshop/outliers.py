"""Detect the numbers that are too good (or bad) to be true, then treat them."""
import numpy as np
import pandas as pd


def inject(s: pd.Series, n: int = 6, mult: float = 8.0, seed: int = 0) -> pd.Series:
    s = s.astype(float).copy()
    rng = np.random.default_rng(seed)
    idx = rng.choice(s.index, n, replace=False)
    s.loc[idx] = float(s.mean()) * mult
    return s


def detect(s: pd.Series, method: str = "iqr", k: float = 1.5):
    if method == "iqr":
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - k * iqr, q3 + k * iqr
    else:  # z-score
        m, sd = s.mean(), s.std()
        lo, hi = m - k * sd, m + k * sd
    return ((s < lo) | (s > hi)), float(lo), float(hi)


def cap(s: pd.Series, lo: float, hi: float) -> pd.Series:
    return s.clip(lo, hi)


def remove(s: pd.Series, mask: pd.Series) -> pd.Series:
    return s[~mask]
