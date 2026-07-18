from streamlit.testing.v1 import AppTest


def test_quantize_page_loads():
    at = AppTest.from_file("pages/53_🧪_Encode_Quantization.py", default_timeout=30).run()
    assert not at.exception
