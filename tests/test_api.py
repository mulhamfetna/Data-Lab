from workshop import api


def test_valid_request_returns_prediction():
    clf, meta = api.build_service()
    r = api.handle_request({"n_orders": 8, "total_qty": 20, "avg_amount": 30}, clf, meta)
    assert r["status"] == 200
    assert r["prediction"] in ("high_value", "regular")
    assert 0.0 <= r["confidence"] <= 1.0


def test_missing_field_returns_400():
    clf, meta = api.build_service()
    r = api.handle_request({"n_orders": 8}, clf, meta)
    assert r["status"] == 400 and "missing" in r["error"]
