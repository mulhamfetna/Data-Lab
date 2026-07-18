from streamlit.testing.v1 import AppTest


def test_charts_page_loads():
    at = AppTest.from_file("pages/84_🧪_Judgment_Charts.py", default_timeout=30).run()
    assert not at.exception
