from streamlit.testing.v1 import AppTest


def test_classify_page_loads():
    at = AppTest.from_file("pages/90_🧪_GenAI_Classify.py", default_timeout=30).run()
    assert not at.exception
