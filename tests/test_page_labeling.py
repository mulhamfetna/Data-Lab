from streamlit.testing.v1 import AppTest


def test_labeling_page_loads():
    at = AppTest.from_file("pages/45_🧪_Label_Interactive.py", default_timeout=30).run()
    assert not at.exception
