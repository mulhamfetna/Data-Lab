from streamlit.testing.v1 import AppTest


def test_byod_page_loads():
    at = AppTest.from_file("pages/77_🧪_Platform_BYOD.py", default_timeout=30).run()
    assert not at.exception
