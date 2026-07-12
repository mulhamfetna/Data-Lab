from workshop import report, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_kpis_shape_and_values():
    k = report.kpis(CLEAN)
    assert k["orders"] == len(CLEAN)
    assert k["revenue"] > 0
    assert 0 <= k["delivered_pct"] <= 100
    assert k["top_product"] and k["top_city"]


def test_summary_text_contains_headline_numbers():
    k = report.kpis(CLEAN)
    txt = report.summary_text(k)
    assert "Nour Store" in txt
    assert k["top_product"] in txt
