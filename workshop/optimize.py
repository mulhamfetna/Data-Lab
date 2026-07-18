"""Optimization — find the price that makes the most money, not just more sales.

The intuition every leader half-knows but rarely quantifies: raise the price and you earn
more per unit but sell fewer; drop it and you sell more but earn less each. Somewhere in
between is the profit peak. This is the simplest, most relatable optimization there is —
and the same maths (an objective with a trade-off) underlies pricing, inventory, staffing,
and ad spend.

We model demand as falling linearly with price, so profit = (price − cost) × demand is a
curve with a single peak we can find by sweeping.
"""
from __future__ import annotations


def demand(price: float, base: float = 1000.0, slope: float = 40.0) -> float:
    """Units sold at a given price — falls as price rises, never below zero."""
    return max(0.0, base - slope * price)


def profit(price: float, cost: float = 5.0,
           base: float = 1000.0, slope: float = 40.0) -> float:
    """Profit = margin per unit × units sold."""
    return (price - cost) * demand(price, base, slope)


def profit_curve(cost: float = 5.0, base: float = 1000.0, slope: float = 40.0,
                 lo: float = 5.0, hi: float = 25.0, step: float = 0.5
                 ) -> list[tuple[float, float]]:
    """(price, profit) pairs across a range of prices."""
    curve = []
    p = lo
    while p <= hi + 1e-9:
        curve.append((round(p, 2), round(profit(p, cost, base, slope), 2)))
        p += step
    return curve


def optimal_price(cost: float = 5.0, base: float = 1000.0, slope: float = 40.0,
                  lo: float = 5.0, hi: float = 25.0, step: float = 0.5) -> dict:
    """The price on the swept curve that maximises profit."""
    curve = profit_curve(cost, base, slope, lo, hi, step)
    best_price, best_profit = max(curve, key=lambda t: t[1])
    return {"price": best_price, "profit": best_profit,
            "units": round(demand(best_price, base, slope)),
            "margin": round(best_price - cost, 2)}
