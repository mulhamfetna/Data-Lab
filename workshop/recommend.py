"""A simple recommender: 'because you bought X, you might like Y' from co-purchases."""
from collections import Counter, defaultdict

from workshop.market_basket import ITEMS, transactions


def cooccurrence(baskets: list[set]) -> dict:
    co = defaultdict(Counter)
    for b in baskets:
        for a in b:
            for c in b:
                if a != c:
                    co[a][c] += 1
    return co


def recommend(item: str, baskets: list[set] | None = None, k: int = 3) -> list[tuple[str, int]]:
    baskets = baskets if baskets is not None else transactions(seed=0)
    co = cooccurrence(baskets)
    return co[item].most_common(k)
