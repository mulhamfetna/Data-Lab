from streamlit.testing.v1 import AppTest


def test_capstone_page_loads():
    at = AppTest.from_file("pages/99_🎓_Capstone.py", default_timeout=30).run()
    assert not at.exception
