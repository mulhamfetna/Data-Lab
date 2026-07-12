"""Export a list of Person into various famous contact formats.

Each exporter returns an Export (bytes + file extension + MIME type) so the UI can
save or download it uniformly.
"""
import csv
import io
import json
from dataclasses import dataclass

from contact_scraper import vcard
from contact_scraper.models import Person


@dataclass(frozen=True)
class Export:
    data: bytes
    ext: str
    mime: str


def _split_name(full: str) -> tuple[str, str]:
    parts = full.strip().split()
    if len(parts) >= 2:
        return " ".join(parts[:-1]), parts[-1]
    return full.strip(), ""


def _rows(people: list[Person]) -> list[dict]:
    """Flat, spreadsheet-friendly rows shared by CSV / Excel / JSON."""
    return [{
        "category": p.category or "",
        "name": p.name,
        "title": p.title or "",
        "org": p.org or "",
        "email": p.email or "",
        "phone": p.phone or "",
        "website": p.website or "",
        "socials": " | ".join(p.socials),
        "bio": p.bio or "",
        "source_url": p.source_url or "",
    } for p in people]


def to_vcard(people: list[Person]) -> Export:
    return Export(vcard.build(people).encode("utf-8"), "vcf", "text/vcard")


def to_csv(people: list[Person]) -> Export:
    rows = _rows(people)
    fields = list(rows[0].keys()) if rows else ["name"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return Export(buf.getvalue().encode("utf-8"), "csv", "text/csv")


def to_json(people: list[Person]) -> Export:
    body = json.dumps(_rows(people), ensure_ascii=False, indent=2)
    return Export(body.encode("utf-8"), "json", "application/json")


def to_excel(people: list[Person]) -> Export:
    import pandas as pd
    buf = io.BytesIO()
    pd.DataFrame(_rows(people)).to_excel(buf, index=False, engine="openpyxl")
    return Export(
        buf.getvalue(), "xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def to_google_csv(people: list[Person]) -> Export:
    """Google Contacts import format (a subset of its standard columns)."""
    fields = ["Name", "Given Name", "Family Name", "Title", "Organization 1 - Name",
              "E-mail 1 - Value", "Phone 1 - Value", "Website 1 - Value",
              "Notes", "Labels"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields)
    writer.writeheader()
    for p in people:
        given, family = _split_name(p.name)
        writer.writerow({
            "Name": p.name,
            "Given Name": given,
            "Family Name": family,
            "Title": p.title or "",
            "Organization 1 - Name": p.org or "",
            "E-mail 1 - Value": p.email or "",
            "Phone 1 - Value": p.phone or "",
            "Website 1 - Value": p.website or "",
            "Notes": p.bio or "",
            "Labels": p.category or "",
        })
    return Export(buf.getvalue().encode("utf-8"), "csv", "text/csv")


# Display label -> exporter. Order controls the dropdown order.
EXPORTERS = {
    "vCard (.vcf) — phone import": to_vcard,
    "Google Contacts (.csv)": to_google_csv,
    "Excel (.xlsx)": to_excel,
    "CSV (.csv)": to_csv,
    "JSON (.json)": to_json,
}
