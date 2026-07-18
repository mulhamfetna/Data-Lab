from workshop import forecasting as fc


def test_history_trends_upward():
    h = fc.history()
    assert h["sales"].iloc[-6:].mean() > h["sales"].iloc[:6].mean()


def test_forecast_shape_and_band():
    h = fc.history()
    f = fc.forecast(h, periods=6)
    assert len(f) == 6
    assert (f["lower"] <= f["forecast"]).all() and (f["forecast"] <= f["upper"]).all()


def test_forecast_continues_trend():
    h = fc.history()
    f = fc.forecast(h, periods=6)
    assert f["forecast"].iloc[-1] > h["sales"].iloc[-1]      # trend keeps climbing
