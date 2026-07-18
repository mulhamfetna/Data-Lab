"""Fraud / anomaly detection: flag the orders that don't fit the pattern."""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def with_anomalies(df: pd.DataFrame, n: int = 8, seed: int = 0) -> pd.DataFrame:
    out = df.copy().reset_index(drop=True)
    rng = np.random.default_rng(seed)
    idx = rng.choice(out.index, n, replace=False)
    out.loc[idx, "quantity"] = rng.integers(30, 80, n)
    out.loc[idx, "amount"] = float(out["amount"].mean()) * rng.uniform(8, 15, n)
    out["injected"] = False
    out.loc[idx, "injected"] = True
    return out


def detect(df: pd.DataFrame, contamination: float = 0.03, seed: int = 0) -> pd.Series:
    X = df[["quantity", "amount"]].to_numpy()
    pred = IsolationForest(contamination=contamination, random_state=seed).fit_predict(X)
    return pd.Series(pred == -1, index=df.index, name="anomaly")
