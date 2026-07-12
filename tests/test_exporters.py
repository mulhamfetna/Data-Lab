import csv
import io
import json

from contact_scraper import exporters
from contact_scraper.models import Person


def _people():
    return [
        Person(name="Garry Tan", title="President & CEO", email="g@yc.com",
               socials=["https://x.com/garrytan"], bio="Runs YC.", category="YC"),
        Person(name="Ada Lovelace", category="YC"),
    ]


def test_registry_has_five_formats():
    assert len(exporters.EXPORTERS) == 5
    labels = list(exporters.EXPORTERS)
    assert any("vCard" in l for l in labels)
    assert any("Excel" in l for l in labels)
    assert any("Google" in l for l in labels)


def test_vcard_export():
    exp = exporters.to_vcard(_people())
    assert exp.ext == "vcf" and exp.mime == "text/vcard"
    assert b"FN:YC \xc2\xb7 Garry Tan" in exp.data  # middot is UTF-8 0xC2 0xB7


def test_csv_export_has_header_and_rows():
    exp = exporters.to_csv(_people())
    assert exp.ext == "csv"
    reader = list(csv.DictReader(io.StringIO(exp.data.decode("utf-8"))))
    assert len(reader) == 2
    assert reader[0]["name"] == "Garry Tan"
    assert reader[0]["email"] == "g@yc.com"
    assert reader[0]["category"] == "YC"


def test_json_export_roundtrips():
    exp = exporters.to_json(_people())
    assert exp.ext == "json"
    data = json.loads(exp.data.decode("utf-8"))
    assert data[0]["name"] == "Garry Tan"
    assert data[0]["socials"] == "https://x.com/garrytan"


def test_google_csv_has_google_columns():
    exp = exporters.to_google_csv(_people())
    rows = list(csv.DictReader(io.StringIO(exp.data.decode("utf-8"))))
    assert rows[0]["Given Name"] == "Garry"
    assert rows[0]["Family Name"] == "Tan"
    assert rows[0]["E-mail 1 - Value"] == "g@yc.com"
    assert rows[0]["Labels"] == "YC"


def test_excel_export_is_valid_xlsx():
    exp = exporters.to_excel(_people())
    assert exp.ext == "xlsx"
    # XLSX files are ZIP archives — magic bytes "PK".
    assert exp.data[:2] == b"PK"
