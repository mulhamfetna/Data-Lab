from streamlit.testing.v1 import AppTest


def test_tracks_page_loads():
    at = AppTest.from_file("pages/34_🎧_Role_Tracks.py", default_timeout=30).run()
    assert not at.exception
