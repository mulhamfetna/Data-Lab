from streamlit.testing.v1 import AppTest


def test_recommend_page_loads():
    at = AppTest.from_file("pages/61_🧪_Model_Recommend.py", default_timeout=30).run()
    assert not at.exception
