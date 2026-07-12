"""Filtering and aggregation over the cleaned Nour Store orders."""
import pandas as pd


def filter_orders(df: pd.DataFrame, cities=None, statuses=None,
                  date_from=None, date_to=None, min_amount=None) -> pd.DataFrame:
    out = df
    if cities:
        out = out[out["city"].isin(cities)]
    if statuses:
        out = out[out["status"].isin(statuses)]
    if date_from is not None:
        out = out[out["order_date"] >= pd.Timestamp(date_from)]
    if date_to is not None:
        out = out[out["order_date"] <= pd.Timestamp(date_to)]
    if min_amount is not None:
        out = out[out["amount"] >= min_amount]
    return out.reset_index(drop=True)


def revenue_by(df: pd.DataFrame, col: str) -> pd.DataFrame:
    g = (df.groupby(col)["amount"].sum().round(2)
         .sort_values(ascending=False).reset_index())
    g.columns = [col, "revenue"]
    return g


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    out = df.dropna(subset=["order_date"]).copy()
    out["month"] = out["order_date"].dt.to_period("M").astype(str)
    g = out.groupby("month")["amount"].sum().round(2).reset_index()
    g.columns = ["month", "revenue"]
    return g.sort_values("month").reset_index(drop=True)
