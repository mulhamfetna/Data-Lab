from workshop import model, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_features_nonempty_and_binary_label():
    X, y = model.build_features(CLEAN)
    assert len(X) > 0 and len(X) == len(y)
    assert set(y.unique()) <= {0, 1}


def test_train_returns_accuracy_and_is_deterministic():
    X, y = model.build_features(CLEAN)
    _, m1 = model.train(X, y, seed=0)
    _, m2 = model.train(X, y, seed=0)
    assert 0.0 <= m1["accuracy"] <= 1.0
    assert m1["accuracy"] == m2["accuracy"]


def test_predict_one_returns_label_and_proba():
    X, y = model.build_features(CLEAN)
    clf, m = model.train(X, y, seed=0)
    out = model.predict_one(clf, {"n_orders": 5, "total_qty": 12, "avg_amount": 20},
                            m["columns"])
    assert out["label"] in (0, 1)
    assert 0.0 <= out["proba"] <= 1.0
