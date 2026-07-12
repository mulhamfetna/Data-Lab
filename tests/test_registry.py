from contact_scraper.sites.registry import SITES, SiteEntry


def test_targets_present_and_manhom_dropped():
    assert len(SITES) == 7
    labels = [s.label for s in SITES]
    assert not any("manhom" in l.lower() for l in labels)
    for expected in ["TED — Speakers", "Nobel Prize — Laureates", "NASA — Astronauts"]:
        assert expected in labels


def test_labels_and_urls():
    by_label = {s.label: s for s in SITES}
    assert "Safierr — Speakers" in by_label
    assert by_label["Safierr — Speakers"].url == "https://safierr.com/speakers/"
    assert any(s.url == "https://www.ycombinator.com/people" for s in SITES)


def test_adapters_are_callable():
    for s in SITES:
        assert callable(s.adapter)


def test_every_entry_has_a_tag():
    for s in SITES:
        assert s.tag


def test_safierr_enriches_yc_does_not():
    by_label = {s.label: s for s in SITES}
    assert callable(by_label["Safierr — Speakers"].enrich)
    assert by_label["Y Combinator — People"].enrich is None
