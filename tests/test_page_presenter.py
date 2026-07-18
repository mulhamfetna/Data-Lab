from streamlit.testing.v1 import AppTest


def test_presenter_page_loads():
    at = AppTest.from_file("pages/78_🧪_Platform_Presenter.py", default_timeout=30).run()
    assert not at.exception
