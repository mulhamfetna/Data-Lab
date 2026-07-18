from workshop import simpson


def test_aggregate_and_subgroups_disagree():
    ov = simpson.overall_rates().set_index("campaign")["rate"]
    assert ov["B"] > ov["A"]                       # B wins overall
    seg = simpson.segment_rates()
    for segment in seg["segment"].unique():
        rows = seg[seg["segment"] == segment].set_index("campaign")["rate"]
        assert rows["A"] > rows["B"]               # A wins every subgroup
