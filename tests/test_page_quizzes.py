from streamlit.testing.v1 import AppTest


def test_quizzes_page_loads():
    at = AppTest.from_file("pages/35_📝_Quizzes.py", default_timeout=30).run()
    assert not at.exception
