import pytest

from workshop import sqlquery, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_group_by_query():
    out = sqlquery.run("SELECT city, COUNT(*) c FROM orders GROUP BY city", CLEAN)
    assert "city" in out.columns and "c" in out.columns
    assert out["c"].sum() == len(CLEAN)


def test_where_filter():
    out = sqlquery.run("SELECT * FROM orders WHERE amount > 20", CLEAN)
    assert (out["amount"] > 20).all()


def test_non_select_rejected():
    with pytest.raises(ValueError):
        sqlquery.run("DROP TABLE orders", CLEAN)


def test_presets_are_selects():
    assert all(v.strip().lower().startswith("select") for v in sqlquery.PRESETS.values())
