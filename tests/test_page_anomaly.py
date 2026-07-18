from streamlit.testing.v1 import AppTest


def test_anomaly_page_loads():
    at = AppTest.from_file("pages/59_🧪_Mine_Anomaly.py", default_timeout=30).run()
    assert not at.exception
