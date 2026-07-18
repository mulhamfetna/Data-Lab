"""Data drift: is today's data still like the data the model was trained on?"""
import numpy as np


def reference(n: int = 2000, seed: int = 0) -> np.ndarray:
    return np.random.default_rng(seed).normal(50, 10, n)


def live(shift: float, n: int = 2000, seed: int = 1) -> np.ndarray:
    return np.random.default_rng(seed).normal(50 + shift, 10, n)


def psi(ref: np.ndarray, cur: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index — the standard drift metric."""
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    ref_pct = np.clip(np.histogram(ref, edges)[0] / len(ref), 1e-4, None)
    cur_pct = np.clip(np.histogram(cur, edges)[0] / len(cur), 1e-4, None)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def report(ref: np.ndarray, cur: np.ndarray) -> dict:
    p = psi(ref, cur)
    verdict = "stable" if p < 0.1 else "moderate drift" if p < 0.25 else "significant drift"
    return {"psi": round(p, 3), "verdict": verdict, "drifted": p >= 0.25}
