import pandas as pd

from workshop import store_data as sd


def test_messy_has_defects():
    df = sd.messy_orders()
    assert df.duplicated().any()                       # duplicate rows exist
    assert df["amount"].isna().any()                   # some missing amounts
    assert (df["quantity"] <= 0).any()                 # some bad quantities
    dates = df["order_date"].dropna().astype(str)
    assert dates.str.contains("-").any() and dates.str.contains("/").any()
    assert df["city"].nunique() > df["city"].str.title().nunique()


def test_messy_is_deterministic():
    assert sd.messy_orders(seed=42).equals(sd.messy_orders(seed=42))


def test_clean_removes_defects():
    clean = sd.clean_orders(sd.messy_orders())
    assert not clean.duplicated().any()
    assert not clean["amount"].isna().any()
    assert (clean["quantity"] > 0).all()
    assert pd.api.types.is_datetime64_any_dtype(clean["order_date"])
    assert (clean["city"] == clean["city"].str.title()).all()


def test_clean_is_smaller_or_equal():
    messy = sd.messy_orders()
    assert len(sd.clean_orders(messy)) <= len(messy)
