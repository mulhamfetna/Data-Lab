from streamlit.testing.v1 import AppTest


def test_fairness_page_loads():
    at = AppTest.from_file("pages/70_🧪_Govern_Fairness.py", default_timeout=30).run()
    assert not at.exception
