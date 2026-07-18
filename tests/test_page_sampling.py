from streamlit.testing.v1 import AppTest


def test_sampling_page_loads():
    at = AppTest.from_file("pages/83_🧪_Judgment_Sampling.py", default_timeout=30).run()
    assert not at.exception
