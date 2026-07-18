"""Guardrails & hallucination — why LLMs make things up, and how to fence them in.

The single most important risk lesson for a leader: an LLM is trained to produce a
*plausible* answer, not necessarily a *true* one. Asked something it doesn't know, an
unguarded model will confidently invent — a "hallucination". The main guardrail is
grounding: force the model to answer only from supplied, trusted text, and to say
"I don't know" otherwise.

The interactive core here is a *grounding checker*: compare an answer against its source
and flag sentences whose facts aren't supported — the tell-tale sign of a hallucination.
"""
from __future__ import annotations

import re

_STOP = {"the", "is", "of", "a", "to", "in", "and", "for", "are", "on", "it", "its", "we",
         "our", "with", "as", "at", "by", "an", "this", "that", "be", "has", "have", "was",
         "will", "can", "your", "you", "they", "or", "from", "not", "no", "yes", "if"}

# A scripted example so the "invented fact" is visible without needing a live model.
SOURCE = ("Nour Store offers refunds within 14 days of delivery. Standard delivery takes "
          "2 to 3 business days. Customer support is open Sunday to Thursday.")
GROUNDED_ANSWER = "You can get a refund within 14 days of delivery."
HALLUCINATED_ANSWER = ("You can get a refund within 30 days, and Nour Store offers free "
                       "international shipping to every country.")


def _content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]{2,}", text.lower()) if w not in _STOP}


def _split(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def sentence_support(sentence: str, source: str) -> float:
    """Fraction of a sentence's content words that also appear in the source."""
    sw = _content_words(sentence)
    if not sw:
        return 1.0
    src = _content_words(source)
    return round(len(sw & src) / len(sw), 2)


def grounding_report(answer: str, source: str, threshold: float = 0.6) -> dict:
    """Flag which answer sentences are supported by the source.

    Returns ``{sentences: [{text, support, supported}], grounded_fraction}``. A sentence
    below the threshold is a likely hallucination — facts not present in the source.
    """
    rows = []
    for s in _split(answer):
        support = sentence_support(s, source)
        rows.append({"text": s, "support": support, "supported": support >= threshold})
    grounded = sum(r["supported"] for r in rows)
    frac = round(grounded / len(rows), 2) if rows else 1.0
    return {"sentences": rows, "grounded_fraction": frac}
