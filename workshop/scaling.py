"""Putting features on a fair scale so no single one dominates a model."""
import pandas as pd


def minmax(s: pd.Series) -> pd.Series:
    rng = s.max() - s.min()
    return (s - s.min()) / rng if rng else s * 0.0


def zscore(s: pd.Series) -> pd.Series:
    sd = s.std()
    return (s - s.mean()) / sd if sd else s * 0.0


def summary(s: pd.Series) -> dict:
    return {"min": round(float(s.min()), 2), "max": round(float(s.max()), 2),
            "mean": round(float(s.mean()), 2), "std": round(float(s.std()), 2)}
