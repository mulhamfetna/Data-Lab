from streamlit.testing.v1 import AppTest


def test_pii_page_loads():
    at = AppTest.from_file("pages/69_🧪_Govern_PII.py", default_timeout=30).run()
    assert not at.exception
