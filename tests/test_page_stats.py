from streamlit.testing.v1 import AppTest


def test_stats_page_loads():
    at = AppTest.from_file("pages/85_🧪_Judgment_Stats.py", default_timeout=30).run()
    assert not at.exception
