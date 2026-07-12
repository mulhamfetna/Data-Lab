from workshop import pipeline as pl, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_star_schema_has_three_tables():
    tables = pl.build_star_schema(CLEAN)
    assert set(tables) == {"dim_customer", "dim_product", "fact_orders"}


def test_dim_product_unique_and_fact_preserves_rows():
    tables = pl.build_star_schema(CLEAN)
    assert tables["dim_product"]["product"].is_unique
    assert len(tables["fact_orders"]) == len(CLEAN)


def test_sqlite_roundtrip(tmp_path):
    tables = pl.build_star_schema(CLEAN)
    db = tmp_path / "nour.db"
    pl.load_to_sqlite(tables, db)
    counts = pl.table_counts(db)
    assert counts["fact_orders"] == len(CLEAN)
    assert counts["dim_product"] == len(tables["dim_product"])
