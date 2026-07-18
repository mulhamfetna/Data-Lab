from streamlit.testing.v1 import AppTest


def test_drift_page_loads():
    at = AppTest.from_file("pages/71_🧪_Govern_Drift.py", default_timeout=30).run()
    assert not at.exception
