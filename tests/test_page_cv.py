from streamlit.testing.v1 import AppTest


def test_cv_page_loads():
    at = AppTest.from_file("pages/64_🧪_Model_ImageClass.py", default_timeout=60).run()
    assert not at.exception
