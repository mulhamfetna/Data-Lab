from workshop import monitoring as mon


def test_accuracy_decays_without_retraining():
    a = mon.accuracy_over_time(weeks=16, retrain_week=None, seed=0)
    assert a[-1] < a[0]


def test_retraining_restores_accuracy():
    a = mon.accuracy_over_time(weeks=16, retrain_week=8, seed=0)
    assert a[8] > a[7]        # sharp recovery at the retrain week
