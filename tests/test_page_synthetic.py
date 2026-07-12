from streamlit.testing.v1 import AppTest


def test_synthetic_page_loads():
    at = AppTest.from_file("pages/12_🧪_Collect_Synthetic.py").run()
    assert not at.exception
    assert len(at.tabs) == 2
