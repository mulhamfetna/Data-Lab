import pytest
from streamlit.testing.v1 import AppTest

PAGES = [
    "pages/14_🧪_Collect_Other_Sources.py",
    "pages/25_🧪_Report.py",
    "pages/30_📊_Roadmap.py",
    "pages/31_📊_Roles.py",
    "pages/32_📊_Career.py",
    "pages/33_📊_Close.py",
]


@pytest.mark.parametrize("path", PAGES)
def test_page_loads(path):
    at = AppTest.from_file(path, default_timeout=30).run()
    assert not at.exception
