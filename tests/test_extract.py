from workshop import extract as ex


def test_extract_fields_pulls_all_parts():
    f = ex.extract_fields(
        "Sara Ahmad, order #4471 for $52.30 on 2026-03-14, sara@example.com, 0955-123-456")
    assert f["order_id"] == "4471"
    assert f["amount"] == "52.30"
    assert f["date"] == "2026-03-14"
    assert f["email"] == "sara@example.com"
    assert f["phone"].replace("-", "").replace(" ", "") == "0955123456"
    assert f["name"] == "Sara Ahmad"


def test_missing_fields_are_none():
    f = ex.extract_fields("just a note with nothing structured in it")
    assert f["order_id"] is None and f["amount"] is None and f["email"] is None


def test_extract_table_shape():
    df = ex.extract_table()
    assert len(df) == len(ex.SAMPLE_MESSAGES)
    assert list(df.columns) == ["name", "order_id", "amount", "date", "phone", "email"]
    assert df.iloc[0]["order_id"] == "4471"


def test_extract_offline_uses_rules(monkeypatch):
    for e in ("GROQ_API_KEY", "OPENROUTER_API_KEY", "HF_TOKEN", "OLLAMA_HOST"):
        monkeypatch.delenv(e, raising=False)
    r = ex.extract("order #900 for $5.00")
    assert r["is_live"] is False
    assert r["fields"]["order_id"] == "900"
