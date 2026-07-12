from dataclasses import dataclass, field


@dataclass
class Person:
    name: str
    title: str | None = None
    org: str | None = None
    bio: str | None = None
    website: str | None = None
    socials: list[str] = field(default_factory=list)
    email: str | None = None
    phone: str | None = None
    photo_url: str | None = None
    photo_b64: str | None = None
    source_url: str | None = None
    category: str | None = None  # site tag; prefixes FN and fills CATEGORIES
