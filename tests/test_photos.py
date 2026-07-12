import base64
import io

from PIL import Image

from contact_scraper import photos


def _png_bytes(w, h):
    buf = io.BytesIO()
    Image.new("RGB", (w, h), (10, 20, 30)).save(buf, format="PNG")
    return buf.getvalue()


def test_encode_downscales_long_edge_to_max():
    b64 = photos.encode_image(_png_bytes(800, 400), max_edge=200)
    img = Image.open(io.BytesIO(base64.b64decode(b64)))
    assert max(img.size) == 200
    assert img.size == (200, 100)


def test_encode_returns_jpeg_base64():
    b64 = photos.encode_image(_png_bytes(50, 50))
    raw = base64.b64decode(b64)
    assert raw[:3] == b"\xff\xd8\xff"  # JPEG magic


def test_embed_returns_none_on_bad_url():
    assert photos.embed("http://127.0.0.1:0/nope.jpg") is None


def test_embed_returns_none_for_none():
    assert photos.embed(None) is None
