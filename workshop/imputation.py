"""Filling missing values without lying — compare imputation strategies."""
import numpy as np
import pandas as pd


def with_missing(s: pd.Series, frac: float = 0.15, seed: int = 0) -> pd.Series:
    s = s.astype(float).copy()
    rng = np.random.default_rng(seed)
    idx = rng.choice(s.index, int(len(s) * frac), replace=False)
    s.loc[idx] = np.nan
    return s


def impute(s: pd.Series, method: str) -> pd.Series:
    if method == "mean":
        return s.fillna(s.mean())
    if method == "median":
        return s.fillna(s.median())
    if method == "zero":
        return s.fillna(0)
    if method == "drop":
        return s.dropna()
    raise ValueError(method)


def summary(s: pd.Series) -> dict:
    return {"count": int(s.count()), "mean": round(float(s.mean()), 2),
            "std": round(float(s.std()), 2), "missing": int(s.isna().sum())}
