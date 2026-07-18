from workshop import cases


def test_has_several_well_formed_cases():
    cs = cases.cases()
    assert len(cs) >= 5
    for c in cs:
        for field in ("company", "icon", "title", "what", "lesson", "epic", "link"):
            assert c[field], f"{field} missing in {c.get('company')}"


def test_links_are_https():
    for c in cases.cases():
        assert c["link"].startswith("https://")


def test_companies_are_unique():
    comps = cases.companies()
    assert len(comps) == len(set(comps))


def test_includes_landmark_stories():
    comps = set(cases.companies())
    assert "Target" in comps and "Amazon" in comps and "Zillow" in comps
