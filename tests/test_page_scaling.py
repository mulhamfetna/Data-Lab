from streamlit.testing.v1 import AppTest


def test_scaling_page_loads():
    at = AppTest.from_file("pages/56_🧪_Encode_Scaling.py", default_timeout=30).run()
    assert not at.exception
