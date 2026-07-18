"""How machines chop text into tokens — the first step of every NLP / LLM pipeline."""
import math
import re


def word_tokens(text: str) -> list[str]:
    """Words and punctuation as separate tokens."""
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)


def char_tokens(text: str) -> list[str]:
    return [c for c in text if not c.isspace()]


def estimate_llm_tokens(text: str) -> int:
    """Rule-of-thumb: LLM tokens ≈ characters / 4 for English (real models use BPE subwords)."""
    return max(1, math.ceil(len(text) / 4))


def stats(text: str) -> dict:
    return {"characters": len(text),
            "words": len(word_tokens(text)),
            "est_llm_tokens": estimate_llm_tokens(text)}
