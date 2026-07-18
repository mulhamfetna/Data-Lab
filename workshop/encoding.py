"""Turning categories like 'Aleppo' into numbers a model can use."""
import pandas as pd


def one_hot(series: pd.Series, prefix: str = "is") -> pd.DataFrame:
    return pd.get_dummies(series, prefix=prefix).astype(int)


def ordinal(series: pd.Series, order: list[str]) -> pd.Series:
    mapping = {v: i for i, v in enumerate(order)}
    return series.map(mapping)
