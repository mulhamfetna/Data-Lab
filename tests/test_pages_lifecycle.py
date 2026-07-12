import pytest
from streamlit.testing.v1 import AppTest

PAGES = [
    "pages/20_🧪_Clean.py",
    "pages/21_🧪_Filter.py",
    "pages/22_🧪_Analyze.py",
    "pages/23_🧪_Engineer.py",
    "pages/24_🧪_Predict.py",
]


@pytest.mark.parametrize("path", PAGES)
def test_page_loads_without_exception(path):
    at = AppTest.from_file(path, default_timeout=30).run()
    assert not at.exception
