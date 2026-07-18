from streamlit.testing.v1 import AppTest


def test_summarize_page_loads():
    at = AppTest.from_file("pages/88_🧪_GenAI_Summarize.py", default_timeout=30).run()
    assert not at.exception
