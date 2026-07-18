"""Time-series forecasting: project the trend forward with an uncertainty band."""
import numpy as np
import pandas as pd


def history(months: int = 36, seed: int = 0) -> pd.DataFrame:
    """Nour Store monthly sales — an upward trend with yearly seasonality and noise."""
    rng = np.random.default_rng(seed)
    t = np.arange(months)
    sales = 200 + 8 * t + 40 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 25, months)
    return pd.DataFrame({"month": t, "sales": sales.round(0)})


def forecast(hist: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    y = hist["sales"].to_numpy()
    x = hist["month"].to_numpy()
    coef = np.polyfit(x, y, 1)
    resid = float((y - np.polyval(coef, x)).std())
    fx = np.arange(x[-1] + 1, x[-1] + 1 + periods)
    fy = np.polyval(coef, fx)
    return pd.DataFrame({"month": fx, "forecast": fy.round(0),
                         "lower": (fy - 1.96 * resid).round(0),
                         "upper": (fy + 1.96 * resid).round(0)})
