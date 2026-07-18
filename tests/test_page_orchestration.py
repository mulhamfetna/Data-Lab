from streamlit.testing.v1 import AppTest


def test_orchestration_page_loads():
    at = AppTest.from_file("pages/75_🧪_Serve_Orchestration.py", default_timeout=30).run()
    assert not at.exception
