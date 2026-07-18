from workshop import optimize as opt


def test_demand_falls_with_price_and_floors_at_zero():
    assert opt.demand(5) > opt.demand(15)
    assert opt.demand(1000) == 0.0


def test_optimal_price_beats_extremes():
    best = opt.optimal_price(cost=5, base=1000, slope=40)
    assert opt.profit(best["price"]) >= opt.profit(5)     # not the lowest price
    assert opt.profit(best["price"]) >= opt.profit(25)    # not the highest price


def test_optimal_matches_analytic_optimum():
    # For linear demand base - slope*p, the profit peak is at (base/slope + cost)/2.
    best = opt.optimal_price(cost=5, base=1000, slope=40, step=0.5)
    analytic = (1000 / 40 + 5) / 2                          # = 15.0
    assert abs(best["price"] - analytic) <= 0.5


def test_curve_is_within_bounds():
    curve = opt.profit_curve(lo=5, hi=25, step=0.5)
    prices = [p for p, _ in curve]
    assert prices[0] == 5.0 and prices[-1] == 25.0
