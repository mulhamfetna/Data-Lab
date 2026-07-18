from streamlit.testing.v1 import AppTest


def test_weak_page_loads():
    at = AppTest.from_file("pages/47_🧪_Label_Weak.py", default_timeout=30).run()
    assert not at.exception
