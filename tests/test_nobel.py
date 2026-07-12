from pathlib import Path

from contact_scraper.sites import nobel

HTML = Path("tests/fixtures/nobel_laureates.html").read_text(encoding="utf-8")


def test_parses_many_laureates():
    people = nobel.parse(HTML, "https://www.nobelprize.org/prizes/lists/all-nobel-prizes/")
    assert len(people) >= 50


def test_laureate_has_name_and_prize_title():
    people = nobel.parse(HTML, "https://www.nobelprize.org/prizes/lists/all-nobel-prizes/")
    names = [p.name for p in people]
    assert "John Clarke" in names
    john = next(p for p in people if p.name == "John Clarke")
    assert "Physics" in john.title
    assert john.org == "The Nobel Prize"


def test_empty_html_returns_empty_list():
    assert nobel.parse("<html></html>", "https://www.nobelprize.org/") == []
