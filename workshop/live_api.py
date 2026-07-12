"""Fetch live currency rates with a bundled offline fallback (never fails on stage)."""
import json
from pathlib import Path

import requests

_CACHE = Path(__file__).resolve().parent.parent / "assets" / "currency_cache.json"


def get_rates(base: str = "USD", timeout: int = 8, cache_path: Path = _CACHE) -> dict:
    """Return {rates, base, date, source} — source is 'live' or 'cached'."""
    try:
        r = requests.get(f"https://api.frankfurter.app/latest?from={base}", timeout=timeout)
        r.raise_for_status()
        d = r.json()
        return {"rates": d["rates"], "base": d.get("base", base),
                "date": d.get("date"), "source": "live"}
    except Exception:
        d = json.loads(Path(cache_path).read_text())
        return {"rates": d["rates"], "base": d.get("base", "USD"),
                "date": d.get("date"), "source": "cached"}
