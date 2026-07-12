from typing import Callable

from contact_scraper.models import Person

# An adapter turns page HTML + its URL into a list of people. Pure function.
Adapter = Callable[[str, str], list[Person]]

# An enricher fills extra fields on a Person from that person's own detail page.
# Pure w.r.t. the network: it receives the already-fetched HTML and mutates the Person.
Enricher = Callable[[str, Person], None]
