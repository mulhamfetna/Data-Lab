from streamlit.testing.v1 import AppTest


def test_indexing_page_loads():
    at = AppTest.from_file("pages/67_🧪_Scale_Indexing.py", default_timeout=30).run()
    assert not at.exception
