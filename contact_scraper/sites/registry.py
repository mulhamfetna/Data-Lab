from dataclasses import dataclass

from contact_scraper.sites.base import Adapter, Enricher
from contact_scraper.sites import safierr, ycombinator, ted, nobel, nasa


@dataclass(frozen=True)
class SiteEntry:
    label: str
    url: str
    tag: str              # short prefix applied to each contact ("Safierr · Name")
    adapter: Adapter
    enrich: Enricher | None = None   # follow each person's detail page, if any


SITES: list[SiteEntry] = [
    SiteEntry("Safierr — Speakers", "https://safierr.com/speakers/",
              "Safierr Speakers", safierr.parse, safierr.enrich),
    SiteEntry("Safierr — Tech Speakers", "https://safierr.com/safierr-tech-speakers/",
              "Safierr Tech", safierr.parse, safierr.enrich),
    SiteEntry("Safierr — Tech Executive Committee",
              "https://safierr.com/safierr-tech-executive-committee/",
              "Safierr Tech Exec", safierr.parse, safierr.enrich),
    SiteEntry("Y Combinator — People", "https://www.ycombinator.com/people",
              "YC", ycombinator.parse, None),
    SiteEntry("TED — Speakers", "https://www.ted.com/speakers",
              "TED", ted.parse, ted.enrich),
    SiteEntry("Nobel Prize — Laureates",
              "https://www.nobelprize.org/prizes/lists/all-nobel-prizes/",
              "Nobel", nobel.parse, None),
    SiteEntry("NASA — Astronauts", "https://en.wikipedia.org/wiki/NASA_Astronaut_Corps",
              "NASA", nasa.parse, None),
]
