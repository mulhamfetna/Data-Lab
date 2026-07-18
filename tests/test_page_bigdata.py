from streamlit.testing.v1 import AppTest


def test_bigdata_page_loads():
    at = AppTest.from_file("pages/65_🧪_Scale_BigData.py", default_timeout=30).run()
    assert not at.exception
