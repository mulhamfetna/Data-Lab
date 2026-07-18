import pandas as pd

from workshop import byod


def test_column_typing_and_summary():
    df = pd.DataFrame({"city": ["A", "B", "A"], "amount": [1.0, 2.0, 3.0], "qty": [1, 2, 3]})
    assert set(byod.numeric_cols(df)) == {"amount", "qty"}
    assert byod.categorical_cols(df) == ["city"]
    s = byod.summary(df)
    assert s == {"rows": 3, "cols": 3, "numeric": 2, "categorical": 1}
