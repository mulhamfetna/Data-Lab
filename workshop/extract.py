"""Structured extraction — pull fields out of messy free text into clean columns.

Half of "AI for business" is really this: turning emails, order notes, and chat messages
into rows a spreadsheet or database can use. Offline we extract with plain regex rules
(no model, no hallucination). With a free provider, a model can do the same for text too
irregular for rules — the page shows the rules already handle the common cases.
"""
from __future__ import annotations

import json
import re

import pandas as pd

from workshop import llm

# A few messy customer messages — the kind of text that arrives by email or chat.
SAMPLE_MESSAGES: list[str] = [
    "Hi, this is Sara Ahmad, order #4471 for $52.30 placed on 2026-03-14. "
    "Reach me on 0955-123-456 or sara.ahmad@example.com about a refund.",
    "Omar here — my order 4489 ($8.00, 2026-03-15) never arrived. phone 0944 998 877.",
    "Please cancel order #4502, total $130.75 from 2026-03-16. email omar.k@shop.co",
]

_PATTERNS = {
    "email": r"[\w.\-]+@[\w\-]+\.[\w.\-]+",
    "phone": r"0\d{2,3}[\s\-]?\d{3}[\s\-]?\d{3}",
    "order_id": r"(?:order\s*#?\s*)(\d{3,})",
    "amount": r"\$\s?(\d+(?:\.\d{2})?)",
    "date": r"\d{4}-\d{2}-\d{2}",
}


def extract_fields(text: str) -> dict:
    """Regex-extract the known fields from one message. Missing fields are None."""
    out: dict[str, str | None] = {}
    for field, pat in _PATTERNS.items():
        m = re.search(pat, text, flags=re.IGNORECASE)
        out[field] = m.group(1) if (m and m.groups()) else (m.group(0) if m else None)
    # A crude name grab: two capitalised words near the start.
    name = re.search(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", text)
    out["name"] = name.group(1) if name else None
    return out


def extract_table(texts: list[str] = SAMPLE_MESSAGES) -> pd.DataFrame:
    """Turn a list of messages into a tidy table, one row per message."""
    cols = ["name", "order_id", "amount", "date", "phone", "email"]
    rows = [{c: extract_fields(t).get(c) for c in cols} for t in texts]
    return pd.DataFrame(rows, columns=cols)


def extract(text: str) -> dict:
    """Live model JSON extraction when a provider is set, regex otherwise.

    Returns ``{fields, is_live}``. Falls back to regex if the model returns non-JSON.
    """
    system = ("Extract these fields as strict JSON with exactly these keys "
              "(use null if absent): name, order_id, amount, date, phone, email. "
              "Return only the JSON object, no prose.")
    live_text, is_live = llm.complete(text, system=system, max_tokens=200)
    if is_live:
        try:
            match = re.search(r"\{.*\}", live_text, flags=re.DOTALL)
            return {"fields": json.loads(match.group(0)), "is_live": True}
        except (ValueError, AttributeError):
            pass  # model didn't return clean JSON — fall through to rules
    return {"fields": extract_fields(text), "is_live": False}
