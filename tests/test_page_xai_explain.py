from streamlit.testing.v1 import AppTest


def test_xai_explain_page_loads():
    at = AppTest.from_file("pages/93_🧪_XAI_Explain.py", default_timeout=60).run()
    assert not at.exception
