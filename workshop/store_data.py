import numpy as np
import pandas as pd

SEED = 42
CITIES = ["Aleppo", "Damascus", "Homs", "Latakia", "Hama"]
PRODUCTS = [
    ("Coffee 250g", 4.5), ("Tea 100g", 2.0), ("Olive Oil 1L", 8.0),
    ("Soap Bar", 1.2), ("Notebook", 1.5), ("Phone Case", 6.0),
]
STATUSES = ["delivered", "pending", "returned", "cancelled"]


def _messy_city(rng, city):
    r = rng.random()
    if r < 0.15:
        return city.lower()
    if r < 0.25:
        return city.upper()
    if r < 0.30:
        return f" {city} "        # stray whitespace
    return city


def messy_orders(seed: int = SEED, n: int = 1000) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        pname, price = PRODUCTS[rng.integers(0, len(PRODUCTS))]
        qty = int(rng.integers(1, 6))
        if rng.random() < 0.03:
            qty = 0 if rng.random() < 0.5 else -qty      # bad quantities
        amount = round(qty * price, 2)
        if rng.random() < 0.05:
            amount = np.nan                              # missing amount
        # mixed date formats
        day = int(rng.integers(1, 28))
        month = int(rng.integers(1, 13))
        if rng.random() < 0.5:
            date = f"2026-{month:02d}-{day:02d}"
        else:
            date = f"{day:02d}/{month:02d}/2026"
        rows.append({
            "order_id": 1000 + i,
            "customer_name": f"Customer {int(rng.integers(1, 200))}",
            "city": _messy_city(rng, CITIES[rng.integers(0, len(CITIES))]),
            "product": pname,
            "quantity": qty,
            "unit_price": price,
            "order_date": date,
            "amount": amount,
            "status": STATUSES[rng.integers(0, len(STATUSES))],
        })
    df = pd.DataFrame(rows)
    # inject ~3% duplicate rows
    dupes = df.sample(frac=0.03, random_state=seed)
    return pd.concat([df, dupes], ignore_index=True)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.drop_duplicates()
    out["city"] = out["city"].str.strip().str.title()
    out["customer_name"] = out["customer_name"].str.strip()
    # parse both date forms
    out["order_date"] = pd.to_datetime(out["order_date"], format="mixed", dayfirst=True,
                                       errors="coerce")
    # recompute missing amounts from quantity * unit_price
    recomputed = (out["quantity"] * out["unit_price"]).round(2)
    out["amount"] = out["amount"].fillna(recomputed)
    # drop non-positive quantities
    out = out[out["quantity"] > 0]
    return out.reset_index(drop=True)
