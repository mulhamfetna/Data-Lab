from streamlit.testing.v1 import AppTest


def test_profiling_page_loads():
    at = AppTest.from_file("pages/48_🧪_Clean_Profiling.py", default_timeout=30).run()
    assert not at.exception
