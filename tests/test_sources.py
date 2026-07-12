from workshop import sources


def test_theme_counts():
    feedback = ["delivery was slow", "great product but slow support", "fast and friendly"]
    themes = {"speed": ["slow", "fast"], "support": ["support", "friendly"]}
    counts = sources.theme_counts(feedback, themes)
    assert counts["speed"] == 3
    assert counts["support"] == 2


def test_survey_summary():
    s = sources.survey_summary([5, 4, 4, 3, 5, 2])
    assert s["n"] == 6
    assert s["mean"] == round((5 + 4 + 4 + 3 + 5 + 2) / 6, 2)
    assert s["top_box_pct"] == round(100 * 4 / 6, 1)   # four responses >= 4
    assert s["distribution"][5] == 2


def test_survey_summary_empty():
    s = sources.survey_summary([])
    assert s["n"] == 0 and s["mean"] == 0.0


def test_raw_survey_has_defects_and_clean_fixes_them():
    raw = sources.raw_survey()
    assert raw.duplicated().any()
    clean = sources.clean_survey(raw)
    assert not clean.duplicated().any()
    for col in ["satisfaction", "recommend", "value_for_money"]:
        assert clean[col].between(1, 5).all()
    assert len(clean) <= len(raw)


def test_code_feedback_turns_text_into_numbers():
    fb = ["slow delivery", "friendly support", "fast and friendly"]
    themes = {"speed": ["slow", "fast"], "support": ["support", "friendly"]}
    coded = sources.code_feedback(fb, themes)
    assert list(coded.columns) == ["comment", "speed", "support"]
    assert coded["speed"].sum() == 2
    assert coded["support"].sum() == 2
    assert set(coded["speed"].unique()) <= {0, 1}
