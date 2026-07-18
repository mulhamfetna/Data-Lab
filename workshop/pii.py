"""PII masking / anonymization: hide the person, keep the pattern."""
import hashlib

import numpy as np
import pandas as pd


def sample(seed: int = 0, n: int = 12) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    first = ["Ahmad", "Sara", "Omar", "Lina", "Nour", "Karim"]
    cities = ["Aleppo", "Damascus", "Homs"]
    rows = []
    for i in range(n):
        f = first[rng.integers(0, len(first))]
        rows.append({"name": f"{f} {chr(65 + int(rng.integers(0, 26)))}.",
                     "email": f"{f.lower()}{int(rng.integers(1, 999))}@mail.com",
                     "phone": f"09{int(rng.integers(10000000, 99999999))}",
                     "city": cities[rng.integers(0, len(cities))],
                     "spend": round(float(rng.uniform(50, 5000)), 2)})
    return pd.DataFrame(rows)


def mask_email(e: str) -> str:
    local, _, domain = e.partition("@")
    shown = local[:1] if local else ""
    return f"{shown}***@{domain}"


def mask_phone(p: str) -> str:
    return ("*" * max(0, len(p) - 2)) + p[-2:]


def hash_id(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:10]


def mask_name(n: str) -> str:
    return " ".join(part[:1] + "." for part in n.split())


def anonymize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["name"] = out["name"].map(mask_name)
    out["email"] = out["email"].map(mask_email)
    out["phone"] = out["phone"].map(mask_phone)
    out["id"] = df["email"].map(hash_id)     # stable pseudonymous key, not reversible
    return out[["id", "name", "email", "phone", "city", "spend"]]
