import pytest

from contact_scraper import engine


def test_fetch_html_raises_fetcherror_on_bad_host():
    with pytest.raises(engine.FetchError):
        engine.fetch_html("http://127.0.0.1:0/", timeout=2)


def test_screenshot_returns_none_when_chrome_path_missing(monkeypatch):
    # Force chrome resolution to a nonexistent binary → must return None, not raise
    monkeypatch.setattr(engine, "CHROME_PATH", "/nonexistent/google-chrome")
    assert engine.screenshot("https://example.com", timeout=3000) is None


@pytest.mark.live
def test_fetch_html_live_smoke():
    html = engine.fetch_html("https://safierr.com/speakers/")
    assert "team__member" in html
