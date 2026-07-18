from streamlit.testing.v1 import AppTest


def test_geospatial_page_loads():
    at = AppTest.from_file("pages/96_🧪_Adv_Geospatial.py", default_timeout=30).run()
    assert not at.exception
