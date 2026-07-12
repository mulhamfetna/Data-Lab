from pathlib import Path

from contact_scraper.sites import ycombinator

HTML = Path("tests/fixtures/ycombinator_people.html").read_text(encoding="utf-8")


def test_parses_many_people():
    people = ycombinator.parse(HTML, "https://www.ycombinator.com/people")
    assert len(people) >= 50


def test_first_person_has_name_and_photo():
    people = ycombinator.parse(HTML, "https://www.ycombinator.com/people")
    p = people[0]
    assert p.name == "Garry Tan"
    assert p.title and "CEO" in p.title
    assert p.photo_url.startswith("https://")


def test_empty_html_returns_empty_list():
    assert ycombinator.parse("<html></html>", "https://www.ycombinator.com/people") == []
