from streamlit.testing.v1 import AppTest


def test_monitoring_page_loads():
    at = AppTest.from_file("pages/74_🧪_Serve_Monitoring.py", default_timeout=30).run()
    assert not at.exception
