from streamlit.testing.v1 import AppTest


def test_glossary_page_loads():
    at = AppTest.from_file("pages/36_📖_Glossary.py", default_timeout=30).run()
    assert not at.exception
