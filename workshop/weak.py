"""Weak supervision: cheap labeling *functions* (rules) vote, instead of hand-labeling each row."""
from workshop.labeling import POOL

POS = ["great", "love", "amazing", "fast", "best", "excellent", "friendly",
       "reliable", "satisfied", "worth", "quick", "smooth", "recommend"]
NEG = ["slow", "poor", "broke", "expensive", "late", "damaged", "bad",
       "never", "wrong", "rude", "forever", "unhelpful"]


def lf_positive(text: str) -> int:
    return 1 if any(w in text for w in POS) else 0     # +1 votes positive, 0 abstains


def lf_negative(text: str) -> int:
    return -1 if any(w in text for w in NEG) else 0    # -1 votes negative, 0 abstains


LFS = [lf_positive, lf_negative]


def apply_lfs(texts: list[str]) -> list[list[int]]:
    return [[lf(t) for lf in LFS] for t in texts]


def majority_vote(row: list[int]):
    s = sum(row)
    if s > 0:
        return 1
    if s < 0:
        return 0
    return None       # abstain / tie


def evaluate(pool=POOL) -> dict:
    texts = [t for t, _ in pool]
    true = [lbl for _, lbl in pool]
    preds = [majority_vote(v) for v in apply_lfs(texts)]
    covered = [(p, t) for p, t in zip(preds, true) if p is not None]
    coverage = len(covered) / len(pool)
    acc = sum(1 for p, t in covered if p == t) / len(covered) if covered else 0.0
    return {"coverage": coverage, "accuracy": acc, "n_covered": len(covered)}
