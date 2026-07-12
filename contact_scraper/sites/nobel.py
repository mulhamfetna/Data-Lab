from urllib.parse import urljoin

from bs4 import BeautifulSoup

from contact_scraper.models import Person

_BASE = "https://www.nobelprize.org"


def parse(html: str, source_url: str) -> list[Person]:
    soup = BeautifulSoup(html, "html.parser")
    people: list[Person] = []
    for card in soup.select(".card-prize"):
        title_el = card.select_one("h3") or card.select_one("h2")
        prize = title_el.get_text(" ", strip=True) if title_el else "Nobel Prize"
        for a in card.select(".card-prize--laureates--links--link"):
            name = a.get_text(" ", strip=True)
            if not name:
                continue
            people.append(Person(
                name=name,
                title=prize,
                org="The Nobel Prize",
                source_url=urljoin(_BASE, a.get("href")) if a.get("href") else source_url,
            ))
    return people
