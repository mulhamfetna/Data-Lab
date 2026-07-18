"""Merging two sources that don't agree — the real work is key reconciliation."""
import numpy as np
import pandas as pd


def sources(n: int = 24, seed: int = 0):
    """Two tables about the same customers, joined on a name key that doesn't match cleanly."""
    rng = np.random.default_rng(seed)
    names = [f"Customer {i}" for i in range(1, n + 1)]
    left = pd.DataFrame({"customer_name": names,
                         "city": rng.choice(["Aleppo", "Homs", "Damascus"], n)})
    # the loyalty system stored names messily (whitespace + casing)
    messy = [f"  {nm.lower()} " if rng.random() < 0.75 else nm for nm in names]
    right = pd.DataFrame({"customer_name": messy,
                          "loyalty": rng.choice(["gold", "silver", "bronze"], n)})
    return left, right


def naive_merge(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    """Join on the raw key — mismatched keys silently drop out (loyalty comes back null)."""
    return left.merge(right, on="customer_name", how="left")


def _norm(s: pd.Series) -> pd.Series:
    return s.str.strip().str.lower()


def reconciled_merge(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    """Normalise the key on both sides first, then join — the reconciliation step."""
    lft, rgt = left.copy(), right.copy()
    lft["_key"] = _norm(lft["customer_name"])
    rgt["_key"] = _norm(rgt["customer_name"])
    return (lft.merge(rgt.drop(columns=["customer_name"]), on="_key", how="left")
            .drop(columns=["_key"]))


def match_rate(merged: pd.DataFrame) -> float:
    return float(merged["loyalty"].notna().mean())
