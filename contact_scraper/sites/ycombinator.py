from bs4 import BeautifulSoup

from contact_scraper.models import Person


def _abs(src: str | None) -> str | None:
    if not src:
        return None
    return "https:" + src if src.startswith("//") else src


def parse(html: str, source_url: str) -> list[Person]:
    soup = BeautifulSoup(html, "html.parser")
    people: list[Person] = []
    for img in soup.select("img.h-20.w-20"):
        card = img.find_parent("li")
        if card is None:
            continue
        # The card holds two ".font-medium" blocks: [0] name, [1] role/title.
        headings = card.select(".font-medium")
        if not headings or not headings[0].get_text(strip=True):
            continue
        name_el = headings[0]
        role_el = headings[1] if len(headings) > 1 else None
        bio_el = card.select_one(".prose")
        people.append(Person(
            name=name_el.get_text(strip=True),
            title=(role_el.get_text(strip=True) if role_el else None),
            bio=(bio_el.get_text(" ", strip=True) if bio_el else None),
            photo_url=_abs(img.get("src")),
            source_url=source_url,
        ))
    return people
