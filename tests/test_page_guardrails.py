from streamlit.testing.v1 import AppTest


def test_guardrails_page_loads():
    at = AppTest.from_file("pages/91_🧪_GenAI_Guardrails.py", default_timeout=30).run()
    assert not at.exception
