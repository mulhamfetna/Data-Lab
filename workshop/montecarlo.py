"""Monte Carlo — model risk by running the future thousands of times.

A single-number forecast ("we'll make $500 profit") hides the thing a leader most needs:
the *range* of what could happen and the *chance* it goes wrong. Monte Carlo answers that
by simulating the outcome thousands of times, each time drawing the uncertain inputs
(demand, margin, costs) from plausible ranges. You get a full distribution — expected
value, a 90% range, and the probability of a loss — instead of one fragile point estimate.

The example: launching a new product. Demand and margin are uncertain; fixed cost is known.
"""
from __future__ import annotations

import numpy as np


def simulate(n: int = 10_000, seed: int = 42,
             units_mean: float = 500.0, units_sd: float = 150.0,
             margin_mean: float = 6.0, margin_sd: float = 1.0,
             fixed_cost: float = 2500.0) -> np.ndarray:
    """Run *n* what-if trials; return the profit outcome of each.

    profit = units_sold × margin_per_unit − fixed_cost, with units and margin drawn from
    normal distributions and floored at zero (you can't sell negative units).
    """
    rng = np.random.default_rng(seed)
    units = np.clip(rng.normal(units_mean, units_sd, n), 0, None)
    margin = np.clip(rng.normal(margin_mean, margin_sd, n), 0, None)
    return units * margin - fixed_cost


def summary(outcomes: np.ndarray) -> dict:
    """Turn the cloud of outcomes into the numbers a leader decides on."""
    return {
        "mean": round(float(np.mean(outcomes)), 0),
        "p5": round(float(np.percentile(outcomes, 5)), 0),
        "p95": round(float(np.percentile(outcomes, 95)), 0),
        "prob_loss": round(float(np.mean(outcomes < 0)), 3),
        "n": int(outcomes.size),
    }


def histogram(outcomes: np.ndarray, bins: int = 40):
    """(bin_centers, counts) for plotting the outcome distribution."""
    counts, edges = np.histogram(outcomes, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    return centers, counts
