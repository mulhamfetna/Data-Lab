from workshop import formats, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_sizes_has_four_formats():
    s = formats.sizes(CLEAN)
    assert set(s) == {"CSV", "JSON", "Excel", "Parquet"}
    assert all(v > 0 for v in s.values())


def test_roundtrip_preserves_row_count():
    rt = formats.roundtrip_rows(CLEAN)
    assert all(v == len(CLEAN) for v in rt.values())


def test_parse_table_from_html():
    html = "<table><tr><th>Product</th><th>Price</th></tr><tr><td>Coffee</td><td>4.5</td></tr></table>"
    df = formats.parse_table(html)
    assert list(df.columns) == ["Product", "Price"]
    assert df.iloc[0]["Product"] == "Coffee"
