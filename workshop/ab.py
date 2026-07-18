"""A/B testing: did the change really work, or is it just noise?"""
import math

import numpy as np


def simulate(n: int, p_a: float, p_b: float, seed: int = 0) -> tuple[int, int]:
    rng = np.random.default_rng(seed)
    return int(rng.binomial(n, p_a)), int(rng.binomial(n, p_b))


def _phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def analyze(n_a: int, c_a: int, n_b: int, c_b: int) -> dict:
    p_a, p_b = c_a / n_a, c_b / n_b
    p = (c_a + c_b) / (n_a + n_b)
    se = math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se if se else 0.0
    pvalue = 2 * (1 - _phi(abs(z)))
    return {"rate_a": round(p_a, 4), "rate_b": round(p_b, 4), "z": round(z, 2),
            "pvalue": round(pvalue, 4), "significant": pvalue < 0.05,
            "lift": round((p_b - p_a) / p_a * 100, 1) if p_a else 0.0}
