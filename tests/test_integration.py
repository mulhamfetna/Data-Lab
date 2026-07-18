from workshop import integration as ig


def test_naive_merge_loses_matches():
    left, right = ig.sources(seed=0)
    naive = ig.naive_merge(left, right)
    assert ig.match_rate(naive) < 1.0        # mismatched keys drop out


def test_reconciled_merge_recovers_all():
    left, right = ig.sources(seed=0)
    fixed = ig.reconciled_merge(left, right)
    assert ig.match_rate(fixed) == 1.0
    assert len(fixed) == len(left)
