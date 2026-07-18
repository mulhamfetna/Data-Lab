from workshop import labeling


def test_needs_both_classes():
    assert labeling.train_and_eval([("loved it", 1), ("amazing", 1)]) is None


def test_learns_from_labels():
    labeled = labeling.POOL[:4] + labeling.POOL[10:14]   # 4 positive + 4 negative
    out = labeling.train_and_eval(labeled)
    assert out is not None
    assert 0.0 <= out["accuracy"] <= 1.0
    assert out["accuracy"] >= 0.6      # a few labels already generalise
    assert out["n_labeled"] == 8


def test_pool_is_balanced():
    pos = sum(lbl for _, lbl in labeling.POOL)
    assert pos == len(labeling.POOL) - pos
