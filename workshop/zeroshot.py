"""LLM-as-classifier — sort text into categories with *no training data*.

The old way to auto-route a support ticket was to collect thousands of labelled examples
and train a model. The new way: just *describe* the categories and let an LLM decide —
"zero-shot". The leader lesson: for many everyday sorting tasks you can skip the whole
data-collection project.

Offline we approximate this with keyword overlap against each category's description
(honest: that's a lexicon, not a real zero-shot model). With a free provider the page
does true zero-shot — the model reads only the label names, no keywords at all.
"""
from __future__ import annotations

import re

from workshop import llm

# Support-ticket categories described by a few cue words each (used only offline).
LABELS: dict[str, str] = {
    "Billing": "payment invoice refund charge price money cost subscription bill overcharged",
    "Shipping": "delivery shipping late arrive package tracking dispatch courier address",
    "Technical": "app website login error bug crash password account loading broken link",
    "Product quality": "quality broken defective size color item wrong damaged expired stale",
}

SAMPLE_TICKETS = [
    "I was charged twice for my subscription this month, please refund the extra amount.",
    "My package still hasn't arrived and the tracking link hasn't updated in days.",
    "I can't log in — the website keeps showing an error after I enter my password.",
    "The coffee beans arrived stale and the bag was torn.",
]


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z]{3,}", text.lower()))


def classify(text: str, labels: dict[str, str] = LABELS) -> dict:
    """Score each label by keyword overlap with the text; return best label + scores.

    Returns ``{label, scores, is_live}``. Ties and empty overlaps fall back to the first
    label with a note-worthy zero score, so the UI can flag low confidence.
    """
    live = _classify_live(text, labels)
    if live is not None:
        return live
    tw = _words(text)
    scores = {name: len(tw & _words(cues)) for name, cues in labels.items()}
    best = max(scores, key=scores.get)
    return {"label": best, "scores": scores, "is_live": False}


def _classify_live(text: str, labels: dict[str, str]) -> dict | None:
    names = list(labels)
    system = ("Classify the user's message into exactly one of these categories: "
              f"{', '.join(names)}. Reply with only the category name, nothing else.")
    out, is_live = llm.complete(text, system=system, max_tokens=20)
    if not is_live:
        return None
    picked = next((n for n in names if n.lower() in (out or "").lower()), names[0])
    return {"label": picked, "scores": {picked: 1}, "is_live": True}
