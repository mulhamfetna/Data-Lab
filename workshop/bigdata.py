"""Out-of-core processing: aggregate data too big for RAM by streaming it in chunks."""
from collections import defaultdict

import numpy as np
import pandas as pd


def make_big(n: int = 500_000, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"city": rng.integers(0, 5, n),
                         "amount": rng.uniform(1, 50, n).round(2)})


def sum_all(df: pd.DataFrame) -> dict:
    """Load everything, aggregate once — simple, but needs the whole table in memory."""
    return {int(k): round(float(v), 2)
            for k, v in df.groupby("city")["amount"].sum().items()}


def sum_chunked(df: pd.DataFrame, chunk: int = 100_000) -> dict:
    """Stream in fixed-size chunks, accumulating — memory stays bounded to one chunk."""
    acc = defaultdict(float)
    for start in range(0, len(df), chunk):
        part = df.iloc[start:start + chunk]
        for k, v in part.groupby("city")["amount"].sum().items():
            acc[int(k)] += float(v)
    return {k: round(v, 2) for k, v in acc.items()}
