from workshop import i18n


def test_translates_both_languages():
    assert i18n.t("title", "en") == "Data to Decisions"
    assert i18n.t("title", "ar") == "من البيانات إلى القرار"


def test_unknown_key_returns_key():
    assert i18n.t("nope_missing", "ar") == "nope_missing"


def test_defaults_to_english():
    assert i18n.t("takeaway") == "Leader takeaway"
