from streamlit.testing.v1 import AppTest


def test_causation_page_loads():
    at = AppTest.from_file("pages/82_🧪_Judgment_Causation.py", default_timeout=30).run()
    assert not at.exception
