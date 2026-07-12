"""Assemble the analysis into a shareable one-page report — the lifecycle's final step."""
import pandas as pd

from workshop import queries as q


def kpis(df: pd.DataFrame) -> dict:
    top_product = q.revenue_by(df, "product").iloc[0]
    top_city = q.revenue_by(df, "city").iloc[0]
    delivered = (df["status"] == "delivered").mean() * 100
    return {
        "orders": int(len(df)),
        "revenue": round(float(df["amount"].sum()), 2),
        "avg_order": round(float(df["amount"].mean()), 2),
        "top_product": str(top_product["product"]),
        "top_city": str(top_city["city"]),
        "delivered_pct": round(float(delivered), 1),
    }


def summary_text(k: dict) -> str:
    return (
        "Nour Store — Data Report\n"
        f"Orders: {k['orders']:,}\n"
        f"Revenue: ${k['revenue']:,.0f}\n"
        f"Average order: ${k['avg_order']:,.2f}\n"
        f"Top product: {k['top_product']}\n"
        f"Top city: {k['top_city']}\n"
        f"Delivered: {k['delivered_pct']}%\n"
    )
