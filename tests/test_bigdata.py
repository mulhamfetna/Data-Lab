from workshop import bigdata as bd


def test_chunked_matches_all_in_memory():
    df = bd.make_big(n=50_000, seed=1)
    a = bd.sum_all(df)
    c = bd.sum_chunked(df, chunk=10_000)
    assert set(a) == set(c)
    for k in a:
        assert abs(a[k] - c[k]) < 0.01       # identical result, bounded memory


def test_make_big_size():
    assert len(bd.make_big(n=1000)) == 1000
