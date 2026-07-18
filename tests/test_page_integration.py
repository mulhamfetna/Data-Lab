from streamlit.testing.v1 import AppTest


def test_integration_page_loads():
    at = AppTest.from_file("pages/43_🧪_Acquire_Integration.py", default_timeout=30).run()
    assert not at.exception
