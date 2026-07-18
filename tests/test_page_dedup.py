from streamlit.testing.v1 import AppTest


def test_dedup_page_loads():
    at = AppTest.from_file("pages/49_🧪_Clean_Dedup.py", default_timeout=30).run()
    assert not at.exception
