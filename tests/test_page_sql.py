from streamlit.testing.v1 import AppTest


def test_sql_page_loads():
    at = AppTest.from_file("pages/42_🧪_Acquire_SQL.py", default_timeout=30).run()
    assert not at.exception
