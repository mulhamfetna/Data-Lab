from workshop import queries as q, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_filter_by_city():
    out = q.filter_orders(CLEAN, cities=["Aleppo"])
    assert set(out["city"].unique()) <= {"Aleppo"}
    assert len(out) < len(CLEAN)


def test_filter_by_min_amount():
    out = q.filter_orders(CLEAN, min_amount=20)
    assert (out["amount"] >= 20).all()


def test_revenue_by_product_sorted_and_correct():
    out = q.revenue_by(CLEAN, "product")
    manual = CLEAN.groupby("product")["amount"].sum().max().round(2)
    assert out["revenue"].iloc[0] == manual
    assert out["revenue"].is_monotonic_decreasing


def test_monthly_revenue_one_row_per_month():
    out = q.monthly_revenue(CLEAN)
    assert out["month"].is_unique
    assert (out["revenue"] > 0).all()
