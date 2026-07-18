from streamlit.testing.v1 import AppTest


def test_streaming_page_loads():
    at = AppTest.from_file("pages/40_🧪_Acquire_Streaming.py", default_timeout=30).run()
    assert not at.exception
