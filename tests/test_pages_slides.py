import pytest
from streamlit.testing.v1 import AppTest

PAGES = ["pages/01_📊_Why_Data.py", "pages/02_📊_The_Lifecycle.py"]


@pytest.mark.parametrize("path", PAGES)
def test_slide_page_loads(path):
    at = AppTest.from_file(path, default_timeout=30).run()
    assert not at.exception
