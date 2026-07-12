from contact_scraper.models import Person


def _esc(value: str) -> str:
    # vCard escaping: backslash, comma, semicolon, newline
    return (value.replace("\\", "\\\\").replace(",", "\\,")
                 .replace(";", "\\;").replace("\n", "\\n"))


def _split_name(full: str) -> str:
    parts = full.strip().split()
    if len(parts) >= 2:
        family = parts[-1]
        given = " ".join(parts[:-1])
    else:
        family, given = full.strip(), ""
    return f"{_esc(family)};{_esc(given)};;;"


def _card(p: Person) -> str:
    # N keeps the real name; FN carries the site prefix so contacts bundle together.
    display = f"{p.category} · {p.name}" if p.category else p.name
    lines = ["BEGIN:VCARD", "VERSION:3.0",
             f"N:{_split_name(p.name)}", f"FN:{_esc(display)}"]
    if p.category:
        lines.append(f"CATEGORIES:{_esc(p.category)}")
    if p.title:
        lines.append(f"TITLE:{_esc(p.title)}")
    if p.org:
        lines.append(f"ORG:{_esc(p.org)}")
    if p.email:
        lines.append(f"EMAIL;TYPE=INTERNET:{_esc(p.email)}")
    if p.phone:
        lines.append(f"TEL;TYPE=CELL:{_esc(p.phone)}")
    for url in [p.website, *p.socials]:
        if url:
            lines.append(f"URL:{_esc(url)}")
    if p.bio:
        lines.append(f"NOTE:{_esc(p.bio)}")
    if p.photo_b64:
        lines.append(f"PHOTO;ENCODING=b;TYPE=JPEG:{p.photo_b64}")
    lines.append("END:VCARD")
    return "\r\n".join(lines)


def build(people: list[Person]) -> str:
    return "\r\n".join(_card(p) for p in people) + "\r\n"


def save(text: str, path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
