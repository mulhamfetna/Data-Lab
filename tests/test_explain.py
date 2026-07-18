import pytest

from workshop import explain


@pytest.fixture(scope="module")
def fitted():
    return explain.trained()


def test_permutation_scores_cover_all_features(fitted):
    clf, X, y, meta = fitted
    scores = explain.permutation_scores(clf, X, y)
    assert set(scores) == set(X.columns)
    # sorted descending
    vals = list(scores.values())
    assert vals == sorted(vals, reverse=True)


def test_a_spend_feature_matters_most(fitted):
    clf, X, y, meta = fitted
    scores = explain.permutation_scores(clf, X, y)
    top = next(iter(scores))
    assert top in {"n_orders", "total_qty", "avg_amount"}   # not a city dummy


def test_explain_prediction_moves_probability_up(fitted):
    clf, X, y, meta = fitted
    cols = meta["columns"]
    rich = {"n_orders": 30, "total_qty": 100, "avg_amount": 55.0}
    rep = explain.explain_prediction(clf, rich, X, cols)
    assert rep["final_proba"] >= rep["baseline_proba"]
    assert set(rep["contributions"]) == set(cols)


def test_top_drivers_returns_nonzero_sorted(fitted):
    clf, X, y, meta = fitted
    rep = explain.explain_prediction(
        clf, {"n_orders": 30, "total_qty": 100, "avg_amount": 55.0}, X, meta["columns"])
    drivers = explain.top_drivers(rep["contributions"], k=3)
    assert len(drivers) <= 3
    mags = [abs(v) for _, v in drivers]
    assert mags == sorted(mags, reverse=True)
