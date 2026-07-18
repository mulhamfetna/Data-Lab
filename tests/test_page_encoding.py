from streamlit.testing.v1 import AppTest


def test_encoding_page_loads():
    at = AppTest.from_file("pages/55_🧪_Encode_Categorical.py", default_timeout=30).run()
    assert not at.exception
