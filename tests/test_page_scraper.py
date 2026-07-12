from streamlit.testing.v1 import AppTest


def test_scraper_page_loads_offline():
    # Page 10 does no network on load (static preview); Scrape Now is user-triggered.
    at = AppTest.from_file("pages/10_🧪_Collect_Scraper.py", default_timeout=30).run()
    assert not at.exception
    assert len(at.selectbox[0].options) == 7   # the 7 scraper sites
