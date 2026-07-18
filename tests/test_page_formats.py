from streamlit.testing.v1 import AppTest


def test_formats_page_loads():
    at = AppTest.from_file("pages/41_🧪_Acquire_Formats.py", default_timeout=30).run()
    assert not at.exception
