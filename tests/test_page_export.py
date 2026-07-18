from streamlit.testing.v1 import AppTest


def test_export_page_loads():
    at = AppTest.from_file("pages/80_🧪_Platform_Export.py", default_timeout=30).run()
    assert not at.exception
