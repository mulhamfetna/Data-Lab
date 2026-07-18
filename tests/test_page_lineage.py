from streamlit.testing.v1 import AppTest


def test_lineage_page_loads():
    at = AppTest.from_file("pages/72_🧪_Govern_Lineage.py", default_timeout=30).run()
    assert not at.exception
