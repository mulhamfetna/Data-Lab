"""Fairness audit: does an outcome treat every group equally — even the qualified ones?"""
import numpy as np
import pandas as pd


def make_data(n: int = 800, seed: int = 0) -> pd.DataFrame:
    """Loan-style approvals where history is biased against one city at equal spend."""
    rng = np.random.default_rng(seed)
    city = rng.choice(["Aleppo", "Homs"], n)
    spend = rng.uniform(0, 100, n)
    bias = np.where(city == "Homs", -18, 0)          # historical bias baked into the labels
    approved = ((spend + bias + rng.normal(0, 8, n)) > 50).astype(int)
    return pd.DataFrame({"city": city, "spend": spend.round(1), "approved": approved})


def audit(df: pd.DataFrame) -> dict:
    overall = df.groupby("city")["approved"].mean()
    qualified = df[df["spend"] > 50]                 # people who *should* qualify on merit
    among_qual = qualified.groupby("city")["approved"].mean()
    return {"overall": overall.round(2).to_dict(),
            "among_qualified": among_qual.round(2).to_dict(),
            "gap": round(float(abs(among_qual.max() - among_qual.min())), 2)}
