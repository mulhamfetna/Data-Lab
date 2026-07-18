from streamlit.testing.v1 import AppTest


def test_journey_page_loads():
    at = AppTest.from_file("pages/79_🧪_Platform_Journey.py", default_timeout=30).run()
    assert not at.exception
