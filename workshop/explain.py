"""Explainability (XAI) — open the black box: *why* did the model decide that?

For a leader, an unexplainable model is a liability: you can't defend it to a customer, a
regulator, or your own board. Two honest, model-agnostic techniques answer two questions:

* **Global** — which inputs drive the model *overall*? Permutation importance: shuffle one
  feature and see how much accuracy drops. A big drop means the model leaned on it.
* **Local** — why *this one* prediction? Occlusion: start from a typical customer and turn
  on this customer's real values one at a time, watching the probability move.

Both are approximations (they ignore some feature interactions), and the UI says so — a
SHAP-style attribution done with plain scikit-learn, no heavy dependency.
"""
from __future__ import annotations

import pandas as pd
from sklearn.inspection import permutation_importance

from workshop import model as m, store_data as sd


def trained(seed: int = 0):
    """Train the Predict model on the shared clean data; return (clf, X, y, meta)."""
    df = sd.clean_orders(sd.messy_orders())
    X, y = m.build_features(df)
    clf, meta = m.train(X, y, seed=seed)
    return clf, X, y, meta


def permutation_scores(clf, X: pd.DataFrame, y, seed: int = 0,
                       n_repeats: int = 8) -> dict[str, float]:
    """Global attribution: mean accuracy drop when each feature is shuffled."""
    r = permutation_importance(clf, X, y, n_repeats=n_repeats, random_state=seed)
    scores = {col: round(float(val), 4) for col, val in zip(X.columns, r.importances_mean)}
    return dict(sorted(scores.items(), key=lambda kv: kv[1], reverse=True))


def _baseline(X: pd.DataFrame, columns: list[str]) -> dict:
    """A 'typical customer' row — the median of each feature."""
    return {c: float(X[c].median()) for c in columns}


def explain_prediction(clf, features: dict, X: pd.DataFrame,
                       columns: list[str]) -> dict:
    """Local attribution for one prediction via occlusion from a typical-customer baseline.

    Returns ``{baseline_proba, final_proba, contributions}`` where each contribution is how
    much that feature's real value moved the high-value probability away from the baseline.
    """
    baseline = _baseline(X, columns)
    base_p = float(clf.predict_proba(pd.DataFrame([baseline]))[0][1])

    contributions = {}
    for c in columns:
        row = dict(baseline)
        row[c] = features.get(c, baseline[c])
        p = float(clf.predict_proba(pd.DataFrame([row]))[0][1])
        contributions[c] = round(p - base_p, 3)

    full = {c: features.get(c, baseline[c]) for c in columns}
    final_p = float(clf.predict_proba(pd.DataFrame([full]))[0][1])
    contributions = dict(sorted(contributions.items(), key=lambda kv: -abs(kv[1])))
    return {"baseline_proba": round(base_p, 3), "final_proba": round(final_p, 3),
            "contributions": contributions}


def top_drivers(contributions: dict[str, float], k: int = 3) -> list[tuple[str, float]]:
    """The k features that moved this prediction the most (either direction)."""
    ranked = sorted(contributions.items(), key=lambda kv: -abs(kv[1]))
    return [(name, val) for name, val in ranked[:k] if val != 0]
