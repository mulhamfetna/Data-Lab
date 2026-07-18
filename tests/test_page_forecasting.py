from streamlit.testing.v1 import AppTest


def test_forecasting_page_loads():
    at = AppTest.from_file("pages/60_🧪_Model_Forecasting.py", default_timeout=30).run()
    assert not at.exception
