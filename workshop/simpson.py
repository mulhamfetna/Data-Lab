"""Simpson's paradox: an aggregate winner that loses in every subgroup."""
import pandas as pd

DATA = pd.DataFrame([
    {"campaign": "A", "segment": "New customers", "reached": 87, "converted": 81},
    {"campaign": "A", "segment": "Returning", "reached": 263, "converted": 192},
    {"campaign": "B", "segment": "New customers", "reached": 270, "converted": 234},
    {"campaign": "B", "segment": "Returning", "reached": 80, "converted": 55},
])


def overall_rates(df: pd.DataFrame = DATA) -> pd.DataFrame:
    g = df.groupby("campaign")[["reached", "converted"]].sum()
    g["rate"] = (g["converted"] / g["reached"] * 100).round(1)
    return g.reset_index()


def segment_rates(df: pd.DataFrame = DATA) -> pd.DataFrame:
    out = df.copy()
    out["rate"] = (out["converted"] / out["reached"] * 100).round(1)
    return out[["campaign", "segment", "rate"]]
