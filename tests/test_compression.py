from workshop import bigdata as bd, compression as cp


def test_parquet_and_gzip_beat_plain_csv():
    df = bd.make_big(n=20_000, seed=0)
    s = cp.sizes(df)
    assert s["Parquet"] < s["CSV"]
    assert s["CSV.gz"] < s["CSV"]


def test_read_speed_reports_both():
    r = cp.read_speed_ms(bd.make_big(n=5_000, seed=0))
    assert "CSV" in r and "Parquet" in r
    assert r["CSV"] >= 0 and r["Parquet"] >= 0
