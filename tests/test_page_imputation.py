from streamlit.testing.v1 import AppTest


def test_imputation_page_loads():
    at = AppTest.from_file("pages/50_🧪_Clean_Imputation.py", default_timeout=30).run()
    assert not at.exception
