from workshop import matrixfactor as mf


def test_matrix_shape_and_planted_tastes():
    m = mf.build_matrix(seed=42)
    assert list(m.columns) == mf.PRODUCTS
    assert len(m) == 12                       # 3 tastes × 4 users
    assert (m.values >= 0).all()


def test_reconstruction_same_shape():
    m = mf.build_matrix(seed=42)
    recon = mf.factorize(m, k=3)
    assert recon.shape == m.shape
    assert list(recon.index) == list(m.index)


def test_recommends_hidden_in_taste_item():
    m = mf.build_matrix(seed=42)
    recon = mf.factorize(m, k=3)
    # coffee_2 bought only Espresso; Coffee was hidden — it should come back on top.
    top, score = mf.recommend("coffee_2", m, recon, n=2)[0]
    assert top == "Coffee"
    assert score > 0


def test_recommends_only_unseen_items():
    m = mf.build_matrix(seed=42)
    recon = mf.factorize(m, k=3)
    recs = mf.recommend("home_0", m, recon, n=3)
    for product, _ in recs:
        assert m.loc["home_0", product] == 0     # never recommends what they already bought
