from workshop import clustering as cl, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_features_one_row_per_customer():
    f = cl.customer_features(CLEAN)
    assert f["customer_name"].is_unique
    assert set(["n_orders", "total_spend", "avg_amount"]).issubset(f.columns)


def test_segment_assigns_k_clusters():
    f = cl.customer_features(CLEAN)
    seg = cl.segment(f, k=4, seed=0)
    assert seg["segment"].nunique() == 4
    assert len(seg) == len(f)


def test_profiles_has_row_per_segment():
    f = cl.customer_features(CLEAN)
    seg = cl.segment(f, k=3, seed=0)
    p = cl.profiles(seg)
    assert len(p) == 3
    assert p["customers"].sum() == len(f)
