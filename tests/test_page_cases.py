from streamlit.testing.v1 import AppTest


def test_cases_page_loads():
    at = AppTest.from_file("pages/37_🗂️_Case_Studies.py", default_timeout=30).run()
    assert not at.exception
