from streamlit.testing.v1 import AppTest


def test_recommender_page_loads():
    at = AppTest.from_file("pages/98_🧪_Adv_Recommender.py", default_timeout=30).run()
    assert not at.exception
