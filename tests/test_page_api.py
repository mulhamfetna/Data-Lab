from streamlit.testing.v1 import AppTest


def test_api_page_loads():
    at = AppTest.from_file("pages/73_🧪_Serve_API.py", default_timeout=60).run()
    assert not at.exception
