"""Sampling bias: ask the wrong people and you get the wrong answer."""
import numpy as np


def population(seed: int = 0, n: int = 5000) -> np.ndarray:
    return np.random.default_rng(seed).normal(50, 15, n).clip(0, 100)


def biased_sample(pop: np.ndarray, bias: float, size: int = 200, seed: int = 1) -> np.ndarray:
    """bias > 0 oversamples high values (e.g., only surveying your happiest customers)."""
    rng = np.random.default_rng(seed)
    weights = (pop - pop.min() + 1.0) ** bias
    weights = weights / weights.sum()
    idx = rng.choice(len(pop), size=size, replace=False, p=weights)
    return pop[idx]


def estimates(pop: np.ndarray, sample: np.ndarray) -> dict:
    return {"true_mean": round(float(pop.mean()), 1),
            "sample_mean": round(float(sample.mean()), 1),
            "gap": round(float(sample.mean() - pop.mean()), 1)}
