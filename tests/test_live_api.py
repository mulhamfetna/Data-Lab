import requests

from workshop import live_api


def test_falls_back_to_cache_on_network_error(monkeypatch):
    def boom(*a, **k):
        raise requests.ConnectionError("no network")
    monkeypatch.setattr(requests, "get", boom)
    out = live_api.get_rates("USD")
    assert out["source"] == "cached"
    assert isinstance(out["rates"], dict) and len(out["rates"]) > 5


def test_cache_file_is_bundled():
    assert live_api._CACHE.exists()
