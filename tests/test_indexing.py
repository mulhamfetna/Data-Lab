from workshop import indexing as ix


def test_index_speeds_up_point_lookup():
    df = ix.make_data(n=40_000, seed=0)
    r = ix.compare(df, key=20_000, repeats=50)
    assert r["same_result"] is True
    assert r["indexed_ms"] < r["unindexed_ms"]
    assert r["speedup"] > 1
