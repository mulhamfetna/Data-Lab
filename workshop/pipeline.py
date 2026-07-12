"""A tiny data-engineering pipeline: flat orders -> star schema -> SQLite."""
import sqlite3

import pandas as pd


def build_star_schema(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    dim_customer = (df[["customer_name", "city"]].drop_duplicates()
                    .reset_index(drop=True))
    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))

    dim_product = (df[["product", "unit_price"]].drop_duplicates()
                   .reset_index(drop=True))
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))

    fact = df.merge(dim_customer, on=["customer_name", "city"]) \
             .merge(dim_product, on=["product", "unit_price"])
    fact_orders = fact[["order_id", "customer_key", "product_key",
                        "quantity", "amount", "order_date", "status"]].copy()
    return {"dim_customer": dim_customer, "dim_product": dim_product,
            "fact_orders": fact_orders}


def load_to_sqlite(tables: dict[str, pd.DataFrame], path) -> None:
    con = sqlite3.connect(path)
    try:
        for name, tbl in tables.items():
            tbl.to_sql(name, con, if_exists="replace", index=False)
    finally:
        con.close()


def table_counts(path) -> dict[str, int]:
    con = sqlite3.connect(path)
    try:
        names = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        return {n: con.execute(f"SELECT COUNT(*) FROM {n}").fetchone()[0] for n in names}
    finally:
        con.close()
