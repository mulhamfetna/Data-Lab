from streamlit.testing.v1 import AppTest


def test_ab_page_loads():
    at = AppTest.from_file("pages/62_🧪_Model_ABTest.py", default_timeout=30).run()
    assert not at.exception
