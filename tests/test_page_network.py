from streamlit.testing.v1 import AppTest


def test_network_page_loads():
    at = AppTest.from_file("pages/97_🧪_Adv_Network.py", default_timeout=30).run()
    assert not at.exception
