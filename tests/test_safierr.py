from pathlib import Path

from contact_scraper.sites import safierr

HTML = Path("tests/fixtures/safierr_speakers.html").read_text(encoding="utf-8")


def test_parses_all_members():
    people = safierr.parse(HTML, "https://safierr.com/speakers/")
    assert len(people) == 68


def test_first_person_fields():
    people = safierr.parse(HTML, "https://safierr.com/speakers/")
    p = people[0]
    assert p.name == "Abdul Hafiz Abdulhafiz"
    assert p.photo_url.endswith(".jpg")
    assert p.source_url.startswith("https://safierr.com/team/")


def test_empty_html_returns_empty_list():
    assert safierr.parse("<html></html>", "https://safierr.com/speakers/") == []


DETAIL = Path("tests/fixtures/safierr_person.html").read_text(encoding="utf-8")


def test_enrich_fills_email_socials_and_bio():
    from contact_scraper.models import Person
    p = Person(name="Abdul Hafiz Abdulhafiz",
               source_url="https://safierr.com/team/abdul-hafiz-abdulhafiz/")
    safierr.enrich(DETAIL, p)
    assert p.email == "aabdulhafiz@kfu.edu.sa"
    assert any("linkedin.com" in s for s in p.socials)
    assert any("x.com" in s for s in p.socials)
    assert p.bio and "Associate Professor" in p.bio


def test_enrich_on_empty_page_is_noop():
    from contact_scraper.models import Person
    p = Person(name="X")
    safierr.enrich("<html></html>", p)
    assert p.email is None
    assert p.socials == []
    assert p.bio is None
