from streamlit.testing.v1 import AppTest


def test_simpson_page_loads():
    at = AppTest.from_file("pages/81_🧪_Judgment_Simpson.py", default_timeout=30).run()
    assert not at.exception
