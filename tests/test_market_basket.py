from workshop import market_basket as mb


def test_finds_planted_associations():
    r = mb.rules(mb.transactions(seed=0))
    coffee_tea = [x for x in r if x["if"] == "Coffee" and x["then"] == "Tea"]
    oil_soap = [x for x in r if x["if"] == "Olive Oil" and x["then"] == "Soap"]
    assert coffee_tea and coffee_tea[0]["lift"] > 1.2
    assert oil_soap and oil_soap[0]["lift"] > 1.0


def test_min_support_filters():
    loose = mb.rules(mb.transactions(seed=0), min_support=0.01)
    strict = mb.rules(mb.transactions(seed=0), min_support=0.15)
    assert len(loose) >= len(strict)
