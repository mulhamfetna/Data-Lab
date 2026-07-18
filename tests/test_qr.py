from workshop import qr


def test_make_qr_returns_png():
    data = qr.make_qr("https://example.com")
    assert data[:8] == b"\x89PNG\r\n\x1a\n"     # PNG magic
    assert len(data) > 100
