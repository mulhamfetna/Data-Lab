import pytest
import requests
from streamlit.testing.v1 import AppTest


def test_datasets_page_loads():
    at = AppTest.from_file("pages/13_🧪_Collect_Datasets.py", default_timeout=30).run()
    assert not at.exception


def test_api_page_loads_offline(monkeypatch):
    # Force the cached path so the test never depends on the network.
    monkeypatch.setattr(requests, "get",
                        lambda *a, **k: (_ for _ in ()).throw(requests.ConnectionError()))
    at = AppTest.from_file("pages/11_🧪_Collect_API.py", default_timeout=30).run()
    assert not at.exception
