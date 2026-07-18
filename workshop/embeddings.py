"""Turning text into numbers you can compare — the idea behind embeddings & search."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CORPUS = [
    "fresh coffee beans roasted daily",
    "premium loose-leaf tea selection",
    "cold-pressed olive oil from the north",
    "fast home delivery across the city",
    "handmade olive soap and skincare",
    "customer support that actually helps",
]


def rank(query: str, corpus: list[str] = CORPUS) -> list[tuple[str, float]]:
    vec = TfidfVectorizer()
    X = vec.fit_transform(corpus + [query])
    sims = cosine_similarity(X[-1], X[:-1])[0]
    return sorted(zip(corpus, (round(float(s), 3) for s in sims)), key=lambda t: -t[1])
