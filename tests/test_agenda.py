from workshop import agenda


def test_agenda_totals_about_four_hours():
    assert 230 <= agenda.total_minutes() <= 250     # ~4 hours
    assert all({"title", "min", "note"} <= set(s) for s in agenda.SEGMENTS)
