import re

from bs4 import BeautifulSoup

from contact_scraper.models import Person

_SOCIAL = re.compile(
    r"linkedin|x\.com|twitter|facebook|instagram|youtube|t\.me|wa\.me|whatsapp", re.I)


def parse(html: str, source_url: str) -> list[Person]:
    soup = BeautifulSoup(html, "html.parser")
    people: list[Person] = []
    for card in soup.select("article.team__member"):
        name_el = card.select_one(".member__name")
        if not name_el or not name_el.get_text(strip=True):
            continue
        link = name_el.select_one("a")
        img = card.select_one(".member__thumbnail img")
        people.append(Person(
            name=name_el.get_text(strip=True),
            photo_url=(img.get("src") if img else None),
            website=(link.get("href") if link else None),
            source_url=(link.get("href") if link else source_url),
        ))
    return people


def enrich(html: str, person: Person) -> None:
    """Fill email, socials, and bio from a person's own team page (mutates in place)."""
    soup = BeautifulSoup(html, "html.parser")
    scope = soup.select_one(".single_team_page") or soup

    mail = scope.select_one('a[href^="mailto:"]')
    if mail and not person.email:
        person.email = mail.get("href")[len("mailto:"):].split("?")[0]

    for a in scope.select("a[href]"):
        href = a.get("href", "")
        if _SOCIAL.search(href) and href not in person.socials:
            person.socials.append(href)

    paras = [p.get_text(" ", strip=True) for p in scope.select("p")
             if len(p.get_text(strip=True)) > 60]
    if paras and not person.bio:
        person.bio = "\n".join(paras)
