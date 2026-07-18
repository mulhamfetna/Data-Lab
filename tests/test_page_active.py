from streamlit.testing.v1 import AppTest


def test_active_page_loads():
    at = AppTest.from_file("pages/46_🧪_Label_Active.py", default_timeout=30).run()
    assert not at.exception
