from workshop import recommend as rc


def test_recommends_co_purchased_item():
    recs = dict(rc.recommend("Coffee"))
    assert "Tea" in recs                       # planted co-purchase
    recs_oil = dict(rc.recommend("Olive Oil"))
    assert "Soap" in recs_oil


def test_k_limits_results():
    assert len(rc.recommend("Coffee", k=2)) <= 2
