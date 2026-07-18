from streamlit.testing.v1 import AppTest


def test_xai_attribution_page_loads():
    at = AppTest.from_file("pages/92_🧪_XAI_Attribution.py", default_timeout=60).run()
    assert not at.exception
