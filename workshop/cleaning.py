"""Composable cleaning steps for the Nour Store orders, plus an issue counter.

Each step fixes one class of defect so the Clean demo can toggle them one at a time.
"""
import pandas as pd

STEP_LABELS = {
    "dedupe": "Remove duplicate rows",
    "normalize_cities": "Standardise city names",
    "parse_dates": "Parse mixed date formats",
    "fill_amounts": "Fill missing amounts",
    "drop_bad_quantity": "Drop invalid quantities",
}


def issues(df: pd.DataFrame) -> dict:
    return {
        "duplicates": int(df.duplicated().sum()),
        "missing_amount": int(df["amount"].isna().sum()),
        "bad_quantity": int((df["quantity"] <= 0).sum()),
        "messy_city": int((df["city"] != df["city"].str.strip().str.title()).sum()),
    }


def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)


def normalize_cities(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["city"] = out["city"].str.strip().str.title()
    out["customer_name"] = out["customer_name"].str.strip()
    return out


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["order_date"] = pd.to_datetime(out["order_date"], format="mixed", dayfirst=True,
                                       errors="coerce")
    return out


def fill_amounts(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    recomputed = (out["quantity"] * out["unit_price"]).round(2)
    out["amount"] = out["amount"].fillna(recomputed)
    return out


def drop_bad_quantity(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["quantity"] > 0].reset_index(drop=True)


_STEPS = {
    "dedupe": dedupe,
    "normalize_cities": normalize_cities,
    "parse_dates": parse_dates,
    "fill_amounts": fill_amounts,
    "drop_bad_quantity": drop_bad_quantity,
}


def apply_steps(df: pd.DataFrame, steps: list[str]) -> pd.DataFrame:
    out = df
    for name in steps:
        out = _STEPS[name](out)
    return out
