from streamlit.testing.v1 import AppTest


def test_tokenize_page_loads():
    at = AppTest.from_file("pages/52_🧪_Encode_Tokenization.py", default_timeout=30).run()
    assert not at.exception
