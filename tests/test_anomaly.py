from workshop import anomaly as an, store_data as sd

CLEAN = sd.clean_orders(sd.messy_orders())


def test_injected_anomalies_are_caught():
    df = an.with_anomalies(CLEAN, n=8, seed=0)
    flag = an.detect(df, contamination=0.03, seed=0)
    caught = (flag & df["injected"]).sum()
    assert caught >= df["injected"].sum() * 0.6      # catches most injected outliers


def test_flag_count_reasonable():
    df = an.with_anomalies(CLEAN, n=8, seed=0)
    flag = an.detect(df, contamination=0.03, seed=0)
    assert 0 < flag.sum() < len(df) * 0.2
