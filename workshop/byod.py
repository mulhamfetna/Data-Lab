"""Bring Your Own Data: quick typing + summary so any uploaded CSV can run the lifecycle."""
import pandas as pd


def numeric_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def categorical_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]


def summary(df: pd.DataFrame) -> dict:
    return {"rows": len(df), "cols": len(df.columns),
            "numeric": len(numeric_cols(df)), "categorical": len(categorical_cols(df))}
