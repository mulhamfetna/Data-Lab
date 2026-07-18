"""Entity resolution: is 'Ahmad Ali' and 'ahmad ali' the same person? Fuzzy-match to decide."""
from difflib import SequenceMatcher

SAMPLE = ["Ahmad Ali", "ahmad ali", "Ahmed Ali", "Sara Nour", "sara  nour",
          "Omar Khaled", "Omar K.", "Lina Haddad", "lina haddad", "Nour Store LLC"]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def duplicate_pairs(names: list[str], threshold: float = 0.85) -> list[tuple[str, str, float]]:
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            s = similarity(names[i], names[j])
            if s >= threshold:
                pairs.append((names[i], names[j], round(s, 2)))
    return sorted(pairs, key=lambda p: -p[2])
