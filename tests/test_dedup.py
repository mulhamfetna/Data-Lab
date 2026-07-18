from workshop import dedup


def test_variants_match_at_high_similarity():
    pairs = dedup.duplicate_pairs(dedup.SAMPLE, threshold=0.9)
    flat = {(a, b) for a, b, _ in pairs}
    assert ("Ahmad Ali", "ahmad ali") in flat or ("ahmad ali", "Ahmad Ali") in flat


def test_threshold_controls_matches():
    loose = dedup.duplicate_pairs(dedup.SAMPLE, threshold=0.6)
    strict = dedup.duplicate_pairs(dedup.SAMPLE, threshold=0.95)
    assert len(loose) >= len(strict)


def test_similarity_bounds():
    assert dedup.similarity("abc", "abc") == 1.0
    assert 0.0 <= dedup.similarity("abc", "xyz") <= 1.0
