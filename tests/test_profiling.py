from workshop import profiling, store_data as sd


def test_profile_flags_messy_data():
    rep = profiling.profile(sd.messy_orders())
    assert rep["rows"] > 0 and rep["cols"] == 9
    assert any("missing" in w for w in rep["warnings"])
    assert any("duplicate" in w for w in rep["warnings"])


def test_profile_clean_data_is_healthier():
    messy = profiling.profile(sd.messy_orders())
    clean = profiling.profile(sd.clean_orders(sd.messy_orders()))
    assert len(clean["warnings"]) < len(messy["warnings"])
    assert "column" in clean["table"].columns
