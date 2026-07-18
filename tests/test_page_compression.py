from streamlit.testing.v1 import AppTest


def test_compression_page_loads():
    at = AppTest.from_file("pages/66_🧪_Scale_Compression.py", default_timeout=30).run()
    assert not at.exception
