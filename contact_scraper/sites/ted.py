from urllib.parse import urljoin

from bs4 import BeautifulSoup

from contact_scraper.models import Person

_BASE = "https://www.ted.com"
import re

_SOCIAL = re.compile(r"twitter|linkedin|x\.com|instagram|facebook\.com/(?!TED)", re.I)


def parse(html: str, source_url: str) -> list[Person]:
    soup = BeautifulSoup(html, "html.parser")
    people: list[Person] = []
    for card in soup.select("a.results__result[href^='/speakers/']"):
        name_el = card.select_one("h4")
        if not name_el or not name_el.get_text(strip=True):
            continue
        # Name is split across spans (first/last) — join with spaces, collapse whitespace.
        name = " ".join(name_el.get_text(" ", strip=True).split())
        full = " ".join(card.get_text(" ", strip=True).split())
        role = full.replace(name, "", 1).strip() or None
        img = card.select_one("img")
        people.append(Person(
            name=name,
            title=role,
            photo_url=(img.get("src") if img else None),
            source_url=urljoin(_BASE, card.get("href")),
        ))
    return people


def enrich(html: str, person: Person) -> None:
    """Fill socials and bio from a TED speaker's own page (mutates in place)."""
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        if _SOCIAL.search(href) and href not in person.socials:
            person.socials.append(href)
    paras = [p.get_text(" ", strip=True) for p in soup.select("p")
             if len(p.get_text(strip=True)) > 80]
    if paras and not person.bio:
        person.bio = "\n".join(paras[:3])
