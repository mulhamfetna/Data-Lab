"""Association rules: 'customers who buy X also buy Y' (support, confidence, lift)."""
import itertools
from collections import Counter

import numpy as np

ITEMS = ["Coffee", "Tea", "Olive Oil", "Soap", "Notebook", "Phone Case"]


def transactions(n: int = 500, seed: int = 0) -> list[set]:
    rng = np.random.default_rng(seed)
    baskets = []
    for _ in range(n):
        b = {it for it in ITEMS if rng.random() < 0.18}
        if "Coffee" in b and rng.random() < 0.65:
            b.add("Tea")                       # planted: coffee → tea
        if "Olive Oil" in b and rng.random() < 0.6:
            b.add("Soap")                      # planted: olive oil → soap
        if b:
            baskets.append(b)
    return baskets


def rules(baskets: list[set], min_support: float = 0.03) -> list[dict]:
    n = len(baskets)
    single, pair = Counter(), Counter()
    for b in baskets:
        for it in b:
            single[it] += 1
        for a, c in itertools.combinations(sorted(b), 2):
            pair[(a, c)] += 1
    out = []
    for (a, c), cnt in pair.items():
        support = cnt / n
        if support < min_support:
            continue
        for x, y in [(a, c), (c, a)]:
            conf = cnt / single[x]
            lift = support / ((single[x] / n) * (single[y] / n))
            out.append({"if": x, "then": y, "support": round(support, 3),
                        "confidence": round(conf, 3), "lift": round(lift, 2)})
    return sorted(out, key=lambda r: -r["lift"])
