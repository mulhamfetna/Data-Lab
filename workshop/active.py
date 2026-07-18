"""Active learning: label the most informative examples first, not random ones."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def _dataset(seed: int, n: int = 200):
    rng = np.random.default_rng(seed)
    x0 = rng.normal([-1.6, 0], 1.1, (n // 2, 2))
    x1 = rng.normal([1.6, 0], 1.1, (n // 2, 2))
    X = np.vstack([x0, x1])
    y = np.array([0] * (n // 2) + [1] * (n // 2))
    idx = rng.permutation(len(X))
    return X[idx], y[idx]


def learning_curve(strategy: str = "random", seed: int = 0, steps: int = 18) -> list[float]:
    """Accuracy after each newly labeled point, for 'random' or 'uncertainty' sampling."""
    Xtr, ytr = _dataset(seed)
    Xte, yte = _dataset(seed + 100)
    rng = np.random.default_rng(seed + 7)
    labeled = [int(np.argmax(ytr == 0)), int(np.argmax(ytr == 1))]  # one per class
    pool = set(range(len(Xtr))) - set(labeled)
    accs = []
    for _ in range(steps):
        clf = LogisticRegression(max_iter=1000).fit(Xtr[labeled], ytr[labeled])
        accs.append(float(accuracy_score(yte, clf.predict(Xte))))
        if not pool:
            break
        pl = list(pool)
        if strategy == "uncertainty":
            probs = clf.predict_proba(Xtr[pl])[:, 1]
            nxt = pl[int(np.argmin(np.abs(probs - 0.5)))]
        else:
            nxt = int(rng.choice(pl))
        labeled.append(nxt)
        pool.discard(nxt)
    return accs
