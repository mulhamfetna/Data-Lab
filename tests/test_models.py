from contact_scraper.models import Person


def test_person_requires_only_name():
    p = Person(name="Ada Lovelace")
    assert p.name == "Ada Lovelace"
    assert p.title is None
    assert p.socials == []


def test_person_socials_are_independent_lists():
    a, b = Person(name="A"), Person(name="B")
    a.socials.append("x.com/a")
    assert b.socials == []
