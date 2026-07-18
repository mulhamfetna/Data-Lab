from workshop import pii


def test_masks_hide_raw_values():
    assert pii.mask_email("ahmad123@mail.com") == "a***@mail.com"
    assert pii.mask_phone("0912345678").endswith("78")
    assert "12345" not in pii.mask_phone("0912345678")
    assert pii.mask_name("Ahmad K.") == "A. K."


def test_hash_is_stable_and_irreversible():
    a = pii.hash_id("ahmad@mail.com")
    assert a == pii.hash_id("ahmad@mail.com")
    assert "ahmad" not in a and len(a) == 10


def test_anonymize_preserves_analytics_columns():
    df = pii.sample()
    anon = pii.anonymize(df)
    assert list(anon["spend"]) == list(df["spend"])       # utility preserved
    assert list(anon["city"]) == list(df["city"])
    assert "@mail.com" in anon["email"].iloc[0] and anon["email"].iloc[0].startswith("")
