import pandas as pd

from workshop import encoding as en


def test_one_hot_has_one_column_per_category():
    s = pd.Series(["Aleppo", "Homs", "Aleppo", "Damascus"])
    oh = en.one_hot(s)
    assert oh.shape == (4, 3)
    assert set(oh.sum()) == {1, 2}      # column sums equal category frequencies


def test_ordinal_maps_by_given_order():
    s = pd.Series(["small", "large", "medium"])
    out = en.ordinal(s, ["small", "medium", "large"])
    assert list(out) == [0, 2, 1]
