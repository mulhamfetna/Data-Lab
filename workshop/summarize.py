"""Text summarization — turn a long block of text into a short brief.

Two flavours, and the difference matters to a leader deciding what to buy:

* **Extractive** (offline, always available) — score each sentence by how many important
  words it carries and keep the top few *verbatim*. Cheap, fast, can't hallucinate, but
  reads like highlighter marks.
* **Abstractive** (live provider) — a model rewrites the gist in fresh words. Smoother, but
  can drift from the source. Shown only when a free provider is configured.

The page shows the compression ratio so the value ("read 20% of the words") is concrete.
"""
from __future__ import annotations

import re

from workshop import llm

_STOP = {"the", "is", "of", "a", "to", "in", "and", "for", "are", "on", "it", "its", "we",
         "our", "was", "were", "with", "as", "at", "by", "an", "this", "that", "be", "has",
         "have", "had", "from", "but", "or", "so", "they", "their", "them", "which", "also"}


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z]{2,}", text.lower()) if w not in _STOP]


def score_sentences(text: str) -> list[tuple[str, float]]:
    """Score each sentence by its share of the document's important words."""
    sentences = split_sentences(text)
    freq: dict[str, int] = {}
    for w in _words(text):
        freq[w] = freq.get(w, 0) + 1
    scored = []
    for s in sentences:
        ws = _words(s)
        score = sum(freq.get(w, 0) for w in ws) / (len(ws) + 1)
        scored.append((s, round(score, 3)))
    return scored


def extractive_summary(text: str, n: int = 3) -> list[str]:
    """Top-n sentences by score, returned in their original document order."""
    scored = score_sentences(text)
    order = {s: i for i, (s, _) in enumerate(scored)}
    top = sorted(scored, key=lambda t: -t[1])[:n]
    return [s for s, _ in sorted(top, key=lambda t: order[t[0]])]


def compression(text: str, summary: str) -> float:
    """Fraction of the original word count the summary keeps (lower = tighter)."""
    orig = len(re.findall(r"\w+", text)) or 1
    return round(len(re.findall(r"\w+", summary)) / orig, 2)


def summarize(text: str, n: int = 3) -> dict:
    """Abstractive summary when a provider is live, extractive otherwise."""
    prompt = (f"Summarize the following text in {n} short sentences for a busy manager:"
              f"\n\n{text}")
    live_text, is_live = llm.complete(prompt, max_tokens=250)
    if is_live:
        summary = live_text
        method = "abstractive"
    else:
        summary = " ".join(extractive_summary(text, n))
        method = "extractive"
    return {"summary": summary, "method": method, "is_live": is_live,
            "compression": compression(text, summary)}
