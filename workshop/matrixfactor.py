"""Matrix factorization — the recommender behind "customers like you also bought".

Simple recommenders count co-occurrence ("people who bought X bought Y"). Matrix
factorization goes deeper: it discovers *hidden tastes* (a "coffee-lover" factor, a
"tea-lover" factor) from the purchase grid, then predicts how much each customer would
like things they haven't tried. It's the idea Netflix made famous — and it fills the gaps
in a sparse purchase table without anyone labelling a single taste.

We plant a few taste groups, hide some purchases, and let NMF rediscover the tastes and
recommend the hidden items back.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import NMF

PRODUCTS = ["Coffee", "Espresso", "Tea", "Green Tea", "Olive Oil", "Soap"]
# Which products each planted taste group tends to buy.
_TASTES = {
    "coffee": ["Coffee", "Espresso"],
    "tea": ["Tea", "Green Tea"],
    "home": ["Olive Oil", "Soap"],
}


def build_matrix(seed: int = 42, per_group: int = 4, hide: float = 0.25) -> pd.DataFrame:
    """A customers × products purchase grid with planted tastes and some purchases hidden.

    Hidden cells (set to 0) are exactly what a good recommender should surface again.
    """
    rng = np.random.default_rng(seed)
    rows, index = [], []
    for taste, liked in _TASTES.items():
        for u in range(per_group):
            counts = {p: 0 for p in PRODUCTS}
            for p in liked:
                counts[p] = int(rng.integers(2, 6))          # buys their taste's items
            # occasional cross-taste purchase
            if rng.random() < 0.2:
                counts[PRODUCTS[rng.integers(0, len(PRODUCTS))]] += 1
            rows.append(counts)
            index.append(f"{taste}_{u}")
    matrix = pd.DataFrame(rows, index=index, columns=PRODUCTS).astype(float)
    # Hide a fraction of the actual purchases so there's something to recommend.
    nonzero = list(zip(*np.nonzero(matrix.values)))
    n_hide = max(1, int(len(nonzero) * hide))
    for i in rng.choice(len(nonzero), size=n_hide, replace=False):
        r, c = nonzero[i]
        matrix.iat[r, c] = 0.0
    return matrix


def factorize(matrix: pd.DataFrame, k: int = 3, seed: int = 0) -> pd.DataFrame:
    """Reconstruct the full preference grid from k latent taste factors (NMF)."""
    model = NMF(n_components=k, init="nndsvda", random_state=seed, max_iter=500)
    W = model.fit_transform(matrix.values)
    H = model.components_
    recon = W @ H
    return pd.DataFrame(recon.round(2), index=matrix.index, columns=matrix.columns)


def recommend(user: str, matrix: pd.DataFrame, reconstructed: pd.DataFrame,
              n: int = 2) -> list[tuple[str, float]]:
    """Top-n products the user hasn't bought yet, ranked by predicted preference."""
    bought = matrix.loc[user]
    preds = reconstructed.loc[user]
    unseen = [(p, float(preds[p])) for p in matrix.columns if bought[p] == 0]
    return sorted(unseen, key=lambda t: -t[1])[:n]
