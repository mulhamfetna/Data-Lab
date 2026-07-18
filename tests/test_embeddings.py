from workshop import embeddings as em


def test_similar_query_ranks_related_text_first():
    ranked = em.rank("i want to buy coffee")
    assert "coffee" in ranked[0][0]
    assert ranked[0][1] >= ranked[-1][1]


def test_scores_in_unit_range():
    for _, s in em.rank("olive oil"):
        assert 0.0 <= s <= 1.0
