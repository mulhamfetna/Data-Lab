"""Helpers for the remaining data-source demos: qualitative + quantitative."""
import numpy as np
import pandas as pd


def raw_survey(seed: int = 7, n: int = 60) -> pd.DataFrame:
    """A raw satisfaction survey with realistic defects (missing, out-of-range, dupes)."""
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        row = {"respondent": i + 1,
               "satisfaction": int(rng.integers(1, 6)),
               "recommend": int(rng.integers(1, 6)),
               "value_for_money": int(rng.integers(1, 6))}
        if rng.random() < 0.10:
            row["satisfaction"] = None                  # missing
        if rng.random() < 0.06:
            row["recommend"] = int(rng.choice([0, 6, 9]))  # out-of-range
        rows.append(row)
    df = pd.DataFrame(rows)
    return pd.concat([df, df.sample(4, random_state=seed)], ignore_index=True)  # dupes


def clean_survey(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates, null out-of-range answers, drop incomplete responses."""
    out = df.drop_duplicates().copy()
    for col in ["satisfaction", "recommend", "value_for_money"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
        out.loc[(out[col] < 1) | (out[col] > 5), col] = np.nan
    out = out.dropna(subset=["satisfaction", "recommend", "value_for_money"])
    for col in ["satisfaction", "recommend", "value_for_money"]:
        out[col] = out[col].astype(int)
    return out.reset_index(drop=True)


def code_feedback(feedback: list[str], themes: dict[str, list[str]]) -> pd.DataFrame:
    """Turn free text (qualitative) into a coded table (quantitative) — one 0/1 per theme."""
    rows = []
    for text in feedback:
        low = text.lower()
        row = {"comment": text}
        for theme, keywords in themes.items():
            row[theme] = int(any(k in low for k in keywords))
        rows.append(row)
    return pd.DataFrame(rows)


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
