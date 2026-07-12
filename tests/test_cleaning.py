import pandas as pd

from workshop import cleaning, store_data as sd

MESSY = sd.messy_orders()


def test_issues_reports_each_defect():
    rep = cleaning.issues(MESSY)
    assert rep["duplicates"] > 0
    assert rep["missing_amount"] > 0
    assert rep["bad_quantity"] > 0
    assert rep["messy_city"] > 0


def test_each_step_clears_its_issue():
    assert cleaning.issues(cleaning.dedupe(MESSY))["duplicates"] == 0
    assert cleaning.issues(cleaning.normalize_cities(MESSY))["messy_city"] == 0
    assert cleaning.issues(cleaning.fill_amounts(MESSY))["missing_amount"] == 0
    assert cleaning.issues(cleaning.drop_bad_quantity(MESSY))["bad_quantity"] == 0


def test_parse_dates_makes_datetime():
    out = cleaning.parse_dates(MESSY)
    assert pd.api.types.is_datetime64_any_dtype(out["order_date"])


def test_apply_all_steps_matches_clean_invariants():
    steps = ["dedupe", "normalize_cities", "parse_dates", "fill_amounts", "drop_bad_quantity"]
    out = cleaning.apply_steps(MESSY, steps)
    rep = cleaning.issues(out)
    assert rep == {"duplicates": 0, "missing_amount": 0, "bad_quantity": 0, "messy_city": 0}
