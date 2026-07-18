"""Simulate a real-time event stream (orders arriving live) + running aggregates."""
import numpy as np
import pandas as pd

from workshop.store_data import CITIES, PRODUCTS


def make_events(n: int = 40, seed: int = 0) -> list[dict]:
    """Generate n order events as if they arrived one at a time."""
    rng = np.random.default_rng(seed)
    events = []
    for i in range(n):
        name, price = PRODUCTS[rng.integers(0, len(PRODUCTS))]
        qty = int(rng.integers(1, 5))
        events.append({
            "event": i + 1,
            "city": CITIES[rng.integers(0, len(CITIES))],
            "product": name,
            "qty": qty,
            "amount": round(qty * price, 2),
        })
    return events


def running_totals(events: list[dict]) -> dict:
    """Aggregate the events seen so far — the essence of stream processing."""
    if not events:
        return {"events": 0, "units": 0, "revenue": 0.0}
    df = pd.DataFrame(events)
    return {"events": len(df), "units": int(df["qty"].sum()),
            "revenue": round(float(df["amount"].sum()), 2)}
