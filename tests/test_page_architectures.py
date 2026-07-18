from streamlit.testing.v1 import AppTest


def test_architectures_page_loads():
    at = AppTest.from_file("pages/68_🧪_Scale_Architectures.py", default_timeout=30).run()
    assert not at.exception
