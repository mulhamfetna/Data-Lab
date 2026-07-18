"""Two statistical traps: how uncertainty shrinks with data, and how testing many things lies."""
import math

import numpy as np


def ci_width(n: int, sd: float = 15.0) -> float:
    """Width of a 95% confidence interval for a mean — narrows as n grows."""
    return round(2 * 1.96 * sd / math.sqrt(n), 2)


def p_hacking(n_tests: int, n: int = 60, seed: int = 0) -> dict:
    """Run n_tests comparisons of two IDENTICAL groups; count 'significant' false positives."""
    rng = np.random.default_rng(seed)
    fp = 0
    for _ in range(n_tests):
        a = rng.normal(0, 1, n)
        b = rng.normal(0, 1, n)               # same distribution — no real difference
        se = math.sqrt(a.var(ddof=1) / n + b.var(ddof=1) / n)
        z = abs(a.mean() - b.mean()) / se
        p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
        if p < 0.05:
            fp += 1
    return {"tests": n_tests, "false_positives": fp, "rate": round(fp / n_tests, 3)}
