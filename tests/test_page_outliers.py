from streamlit.testing.v1 import AppTest


def test_outliers_page_loads():
    at = AppTest.from_file("pages/51_🧪_Clean_Outliers.py", default_timeout=30).run()
    assert not at.exception
