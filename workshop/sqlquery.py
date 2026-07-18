"""Query the Nour Store orders with real SQL against an in-memory SQLite database."""
import sqlite3

import pandas as pd

PRESETS = {
    "Top products by revenue":
        "SELECT product, ROUND(SUM(amount),2) AS revenue\nFROM orders\nGROUP BY product\nORDER BY revenue DESC",
    "Orders per city":
        "SELECT city, COUNT(*) AS orders\nFROM orders\nGROUP BY city\nORDER BY orders DESC",
    "Big delivered orders":
        "SELECT order_id, city, product, amount\nFROM orders\nWHERE status='delivered' AND amount > 20\nORDER BY amount DESC\nLIMIT 20",
}


def run(sql: str, df: pd.DataFrame) -> pd.DataFrame:
    """Run a read-only SELECT against the orders table (loaded from df)."""
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed in this demo.")
    con = sqlite3.connect(":memory:")
    try:
        df.to_sql("orders", con, index=False)
        return pd.read_sql_query(sql, con)
    finally:
        con.close()
