from pathlib import Path

from contact_scraper.models import Person
from contact_scraper.sites import ted

LISTING = Path("tests/fixtures/ted_speakers.html").read_text(encoding="utf-8")
DETAIL = Path("tests/fixtures/ted_person.html").read_text(encoding="utf-8")


def test_parses_speaker_cards():
    people = ted.parse(LISTING, "https://www.ted.com/speakers")
    assert len(people) >= 20


def test_first_speaker_fields():
    people = ted.parse(LISTING, "https://www.ted.com/speakers")
    p = people[0]
    assert p.name == "Jennifer Aaker"
    assert p.title and "scientist" in p.title.lower()
    assert p.source_url.startswith("https://www.ted.com/speakers/")
    assert p.photo_url and p.photo_url.startswith("http")


def test_enrich_adds_socials_and_bio():
    p = Person(name="Jennifer Aaker",
               source_url="https://www.ted.com/speakers/jennifer_aaker")
    ted.enrich(DETAIL, p)
    assert any("twitter" in s or "linkedin" in s for s in p.socials)
    assert p.bio


def test_empty_html_returns_empty_list():
    assert ted.parse("<html></html>", "https://www.ted.com/speakers") == []
