"""Correlation ≠ causation: a strong link that's really a hidden common cause."""
import numpy as np
import pandas as pd


def data(seed: int = 0, n: int = 200) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    temp = rng.uniform(10, 40, n)                 # the hidden confounder
    ice_cream = temp * 3 + rng.normal(0, 8, n)
    drownings = temp * 0.5 + rng.normal(0, 3, n)
    return pd.DataFrame({"temperature": temp.round(1),
                         "ice_cream_sales": ice_cream.round(1),
                         "drownings": drownings.round(1)})


def correlations(df: pd.DataFrame) -> dict:
    return {
        "ice_cream_vs_drownings": round(float(df["ice_cream_sales"].corr(df["drownings"])), 2),
        "temp_vs_ice_cream": round(float(df["temperature"].corr(df["ice_cream_sales"])), 2),
        "temp_vs_drownings": round(float(df["temperature"].corr(df["drownings"])), 2),
    }
