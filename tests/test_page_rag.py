from streamlit.testing.v1 import AppTest


def test_rag_page_loads():
    at = AppTest.from_file("pages/87_🧪_GenAI_RAG.py", default_timeout=30).run()
    assert not at.exception
