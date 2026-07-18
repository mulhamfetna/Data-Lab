"""Why a query is instant or slow: the same point-lookup with and without an index."""
import sqlite3
import time

import numpy as np
import pandas as pd

_QUERY = "SELECT amount FROM t WHERE order_id = ?"


def make_data(n: int = 300_000, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"order_id": np.arange(n),
                         "amount": rng.uniform(1, 50, n).round(2)})


def compare(df: pd.DataFrame, key: int, repeats: int = 200) -> dict:
    def run(indexed: bool) -> tuple[float, object]:
        con = sqlite3.connect(":memory:")
        df.to_sql("t", con, index=False)
        if indexed:
            con.execute("CREATE INDEX idx_id ON t(order_id)")
        t0 = time.time()
        result = None
        for _ in range(repeats):
            result = con.execute(_QUERY, (key,)).fetchone()
        dt = (time.time() - t0) * 1000
        con.close()
        return dt, result

    t_no, res_no = run(False)
    t_yes, res_yes = run(True)
    return {"unindexed_ms": round(t_no, 1), "indexed_ms": round(t_yes, 1),
            "speedup": round(t_no / t_yes, 1) if t_yes else 0.0,
            "same_result": res_no == res_yes}
