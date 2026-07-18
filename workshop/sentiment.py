"""Lexicon sentiment scoring: are the reviews happy?"""
from collections import Counter

from workshop.weak import NEG, POS


def score(text: str) -> int:
    low = text.lower()
    return sum(w in low for w in POS) - sum(w in low for w in NEG)


def label(text: str) -> str:
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


def summarize(texts: list[str]) -> dict:
    return dict(Counter(label(t) for t in texts))
