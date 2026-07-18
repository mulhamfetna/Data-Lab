from workshop import glossary as gl


def test_every_entry_is_bilingual_and_complete():
    assert len(gl.GLOSSARY) >= 25
    for e in gl.GLOSSARY:
        assert e["en"] and e["ar"] and e["def_en"] and e["def_ar"]
        # Arabic fields actually contain Arabic script
        assert any("؀" <= ch <= "ۿ" for ch in e["ar"])
        assert any("؀" <= ch <= "ۿ" for ch in e["def_ar"])


def test_english_search():
    hits = gl.search("hallucination")
    assert any(e["en"] == "Hallucination" for e in hits)


def test_arabic_search():
    hits = gl.search("سببية")
    assert any(e["en"] == "Causation" for e in hits)


def test_empty_query_returns_all():
    assert len(gl.search("")) == len(gl.GLOSSARY)


def test_no_match_returns_empty():
    assert gl.search("zzzznotaterm") == []


def test_terms_are_unique():
    assert len(gl.terms()) == len(set(gl.terms()))
