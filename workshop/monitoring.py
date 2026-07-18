"""The MLOps loop: watch accuracy decay, retrain, redeploy."""
import numpy as np


def accuracy_over_time(weeks: int = 16, retrain_week: int | None = None,
                       seed: int = 0) -> list[float]:
    rng = np.random.default_rng(seed)
    acc = 0.94
    out = []
    for w in range(weeks):
        acc -= 0.02 + rng.uniform(0, 0.004)     # silent decay as the world drifts
        if retrain_week is not None and w == retrain_week:
            acc = 0.94                           # retrain restores performance
        out.append(round(max(acc, 0.5), 3))
    return out
