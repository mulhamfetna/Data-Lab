"""RAG — retrieval-augmented Q&A: ground an LLM in *your own* documents.

The lesson for a leader: a general model doesn't know your refund policy. RAG fixes that
without retraining — you *retrieve* the few relevant snippets from your documents and hand
them to the model as context, so the answer is grounded in your facts, not the model's guess.

Offline we do the retrieval for real (TF-IDF + cosine, the same idea as the Embeddings demo)
and answer *extractively* — quoting the best-matching snippet. With a provider configured,
the same retrieved snippets are handed to a live model to phrase the answer, still grounded.
"""
from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from workshop import llm

# Tiny stopword list + naive singular-izer so "refund" matches "refunds" without a heavy
# NLP dependency. Enough to make word-overlap retrieval feel robust in a live demo.
_STOP = {"the", "is", "of", "how", "do", "get", "a", "i", "to", "in", "and", "for", "are",
         "on", "you", "your", "we", "our", "it", "its", "if", "any", "or", "within", "an",
         "this", "that", "have", "does", "can", "my", "me", "what", "when", "where", "with"}


def _tokens(text: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z]{2,}", text.lower()):
        if w.endswith("s") and len(w) > 3:
            w = w[:-1]                      # refunds -> refund, days -> day
        if w not in _STOP:
            out.append(w)
    return out


def _vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(tokenizer=_tokens, token_pattern=None)

# A tiny "company knowledge base" — Nour Store's policy snippets.
KNOWLEDGE_BASE: list[str] = [
    "Refunds are available within 14 days of delivery if the item is unused and in its "
    "original packaging. Refunds are processed to the original payment method within 5 days.",
    "Standard delivery across the city takes 2 to 3 business days. Express same-day delivery "
    "is available for orders placed before 11am, for an extra fee of 3 dollars.",
    "Loyalty points: customers earn 1 point per dollar spent. 100 points can be redeemed for "
    "a 5 dollar discount on any future order.",
    "Our coffee beans are roasted in small batches every morning and ship the same day, so "
    "they arrive fresh. Whole-bean and ground options are available at checkout.",
    "Customer support is available 9am to 6pm, Sunday to Thursday, by phone and by chat. "
    "Orders can be cancelled free of charge any time before they are shipped.",
    "We ship only within the country. International shipping is not currently offered, though "
    "we are planning to add it next year.",
]

GROUNDED_SYSTEM = (
    "You answer strictly and only from the CONTEXT provided by the user. "
    "If the context does not contain the answer, reply exactly: "
    "'I don't have that information in the documents.' Keep answers to one or two sentences.")


def retrieve(query: str, docs: list[str] = KNOWLEDGE_BASE, k: int = 2
             ) -> list[tuple[str, float]]:
    """Return the top-k document snippets most relevant to the query, with scores."""
    vec = _vectorizer()
    X = vec.fit_transform(docs + [query])
    sims = cosine_similarity(X[-1], X[:-1])[0]
    ranked = sorted(zip(docs, (round(float(s), 3) for s in sims)), key=lambda t: -t[1])
    return ranked[:k]


def answer(query: str, docs: list[str] = KNOWLEDGE_BASE, k: int = 2) -> dict:
    """Retrieve context, then answer grounded in it.

    Returns ``{retrieved, answer, is_live, grounded}``. ``grounded`` is False when even the
    best snippet is essentially irrelevant (top score ~0) — the honest 'I don't know' case.
    """
    retrieved = retrieve(query, docs, k)
    top_score = retrieved[0][1] if retrieved else 0.0
    grounded = top_score > 0.03
    context = "\n".join(f"- {snippet}" for snippet, _ in retrieved)

    if not grounded:
        return {"retrieved": retrieved, "grounded": False, "is_live": False,
                "answer": "I don't have that information in the documents."}

    prompt = f"CONTEXT:\n{context}\n\nQUESTION: {query}"
    text, is_live = llm.complete(prompt, system=GROUNDED_SYSTEM, max_tokens=200)
    if is_live:
        return {"retrieved": retrieved, "grounded": True, "is_live": True, "answer": text}
    # Offline: extractive answer — quote the best-matching snippet verbatim.
    return {"retrieved": retrieved, "grounded": True, "is_live": False,
            "answer": retrieved[0][0]}
