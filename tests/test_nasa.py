from pathlib import Path

from contact_scraper.sites import nasa

HTML = Path("tests/fixtures/nasa_astronauts.html").read_text(encoding="utf-8")


def test_parses_active_roster():
    people = nasa.parse(HTML, "https://en.wikipedia.org/wiki/NASA_Astronaut_Corps")
    assert len(people) >= 30


def test_astronaut_fields():
    people = nasa.parse(HTML, "https://en.wikipedia.org/wiki/NASA_Astronaut_Corps")
    names = [p.name for p in people]
    assert "Nichole Ayers" in names
    a = next(p for p in people if p.name == "Nichole Ayers")
    assert a.title == "NASA Astronaut"


def test_header_rows_excluded():
    people = nasa.parse(HTML, "https://en.wikipedia.org/wiki/NASA_Astronaut_Corps")
    assert all(p.name.lower() != "astronaut" for p in people)


def test_empty_html_returns_empty_list():
    assert nasa.parse("<html></html>", "https://en.wikipedia.org/") == []
