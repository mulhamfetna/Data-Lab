from streamlit.testing.v1 import AppTest


def test_optimize_page_loads():
    at = AppTest.from_file("pages/94_🧪_Adv_Optimize.py", default_timeout=30).run()
    assert not at.exception
