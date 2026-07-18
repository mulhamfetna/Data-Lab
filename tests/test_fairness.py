from workshop import fairness as fr


def test_audit_detects_disparity():
    a = fr.audit(fr.make_data(seed=0))
    assert a["gap"] > 0.15                       # meaningful unequal treatment
    # the disadvantaged group is approved less even when qualified
    assert a["among_qualified"]["Homs"] < a["among_qualified"]["Aleppo"]
