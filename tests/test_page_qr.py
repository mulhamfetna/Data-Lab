from streamlit.testing.v1 import AppTest


def test_qr_page_loads():
    at = AppTest.from_file("pages/76_🧪_Share_QR.py", default_timeout=30).run()
    assert not at.exception
