from streamlit.testing.v1 import AppTest


def test_prompt_page_loads():
    at = AppTest.from_file("pages/86_🧪_GenAI_Prompt.py", default_timeout=30).run()
    assert not at.exception
