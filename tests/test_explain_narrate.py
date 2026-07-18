from workshop import explain


def test_friendly_labels():
    assert explain.friendly("n_orders") == "number of orders"
    assert "Aleppo" in explain.friendly("city_Aleppo")


def test_narrate_produces_sentences():
    contribs = {"n_orders": 0.4, "avg_amount": -0.1, "total_qty": 0.0}
    lines = explain.narrate(contribs, k=3)
    assert any("raised" in l for l in lines)
    assert any("lowered" in l for l in lines)
    # the zero-contribution feature is dropped
    assert not any("total items" in l for l in lines)


def test_narrate_orders_by_magnitude():
    contribs = {"a": 0.1, "b": -0.5, "c": 0.2}
    lines = explain.narrate(contribs, k=3)
    assert "0.50" in lines[0] or "-0.50" in lines[0]
