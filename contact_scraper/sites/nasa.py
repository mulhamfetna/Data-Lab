from urllib.parse import urljoin

from bs4 import BeautifulSoup

from contact_scraper.models import Person

_BASE = "https://en.wikipedia.org"


def parse(html: str, source_url: str) -> list[Person]:
    soup = BeautifulSoup(html, "html.parser")
    people: list[Person] = []
    for table in soup.select("table.wikitable"):
        for row in table.select("tr"):
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue
            name = cells[0].get_text(" ", strip=True)
            if not name or name.lower() == "astronaut":
                continue
            note = cells[1].get_text(" ", strip=True)
            link = cells[0].select_one("a[href^='/wiki/']")
            people.append(Person(
                name=name,
                title="NASA Astronaut",
                bio=note or None,
                source_url=(urljoin(_BASE, link.get("href")) if link else source_url),
            ))
    return people
