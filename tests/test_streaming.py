from workshop import streaming


def test_make_events_shape_and_determinism():
    a = streaming.make_events(n=25, seed=1)
    b = streaming.make_events(n=25, seed=1)
    assert len(a) == 25
    assert a == b
    assert set(a[0]) == {"event", "city", "product", "qty", "amount"}


def test_running_totals_accumulates():
    events = streaming.make_events(n=10, seed=2)
    tot = streaming.running_totals(events)
    assert tot["events"] == 10
    assert tot["units"] == sum(e["qty"] for e in events)
    assert round(tot["revenue"], 2) == round(sum(e["amount"] for e in events), 2)


def test_running_totals_empty():
    assert streaming.running_totals([]) == {"events": 0, "units": 0, "revenue": 0.0}
