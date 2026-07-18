"""Generate a QR code image for a URL — so an audience can open the app on their phones."""
import io

import qrcode


def make_qr(url: str) -> bytes:
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
