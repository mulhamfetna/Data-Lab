"""Helpers for the remaining data-source demos: qualitative + quantitative."""


def theme_counts(feedback: list[str], themes: dict[str, list[str]]) -> dict[str, int]:
    """Count how many feedback strings mention each theme (by keyword)."""
    counts = {theme: 0 for theme in themes}
    for text in feedback:
        low = text.lower()
        for theme, keywords in themes.items():
            if any(k in low for k in keywords):
                counts[theme] += 1
    return counts


def survey_summary(responses: list[int]) -> dict:
    """Summarise 1–5 Likert survey responses into numbers you can act on."""
    n = len(responses)
    if n == 0:
        return {"n": 0, "mean": 0.0, "top_box_pct": 0.0, "distribution": {i: 0 for i in range(1, 6)}}
    dist = {i: responses.count(i) for i in range(1, 6)}
    top_box = sum(1 for r in responses if r >= 4)
    return {
        "n": n,
        "mean": round(sum(responses) / n, 2),
        "top_box_pct": round(100 * top_box / n, 1),
        "distribution": dist,
    }
