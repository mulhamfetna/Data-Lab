from contact_scraper.models import Person
from contact_scraper import vcard


def test_minimal_card_has_required_fields():
    out = vcard.build([Person(name="Ada Lovelace")])
    assert out.startswith("BEGIN:VCARD")
    assert "VERSION:3.0" in out
    assert "FN:Ada Lovelace" in out
    assert "N:Lovelace;Ada;;;" in out
    assert out.rstrip().endswith("END:VCARD")


def test_optional_fields_emitted_only_when_present():
    out = vcard.build([Person(name="Ada", title="CTO", org="Analytical Engines",
                              email="ada@x.io", website="https://x.io",
                              socials=["https://x.com/ada"], bio="Pioneer.")])
    assert "TITLE:CTO" in out
    assert "ORG:Analytical Engines" in out
    assert "EMAIL;TYPE=INTERNET:ada@x.io" in out
    assert "URL:https://x.io" in out
    assert "URL:https://x.com/ada" in out
    assert "NOTE:Pioneer." in out


def test_absent_fields_are_omitted():
    out = vcard.build([Person(name="Ada")])
    assert "TITLE:" not in out
    assert "EMAIL" not in out
    assert "PHOTO" not in out


def test_photo_embedded_when_present():
    out = vcard.build([Person(name="Ada", photo_b64="QUJD")])
    assert "PHOTO;ENCODING=b;TYPE=JPEG:QUJD" in out


def test_multiple_people_produce_multiple_blocks():
    out = vcard.build([Person(name="A"), Person(name="B")])
    assert out.count("BEGIN:VCARD") == 2
    assert out.count("END:VCARD") == 2


def test_special_chars_escaped():
    out = vcard.build([Person(name="A,B; Co\\X")])
    assert "FN:A\\,B\\; Co\\\\X" in out


def test_category_prefixes_fn_and_keeps_real_n():
    out = vcard.build([Person(name="Garry Tan", category="YC")])
    assert "FN:YC · Garry Tan" in out
    assert "N:Tan;Garry;;;" in out          # structured name stays clean
    assert "CATEGORIES:YC" in out


def test_no_category_leaves_fn_unprefixed():
    out = vcard.build([Person(name="Garry Tan")])
    assert "FN:Garry Tan" in out
    assert "CATEGORIES" not in out
