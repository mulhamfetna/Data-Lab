"""Case-study cards — the real-world stories behind every lesson in the lab.

Abstract lessons land when they're attached to a name a leader recognises. These are
well-documented, sourced stories — triumphs and disasters — each tied to the lab stage it
illustrates, so "sampling bias" or "data drift" stops being a term and becomes Amazon's
recruiting tool or Zillow's home-flipping collapse.
"""
from __future__ import annotations

CASES: list[dict[str, str]] = [
    {
        "company": "Target",
        "icon": "🎯",
        "title": "Predicting pregnancy from shopping habits",
        "what": "Target built a model that spotted likely pregnancies from buying patterns "
                "(unscented lotion, supplements) and mailed baby coupons — reportedly before "
                "one teenager's family knew.",
        "lesson": "Prediction without consent is a privacy and trust minefield, even when the "
                  "model is accurate.",
        "epic": "Predict / Govern",
        "link": "https://www.nytimes.com/2012/02/19/magazine/shopping-habits.html",
    },
    {
        "company": "Zillow",
        "icon": "🏠",
        "title": "When the pricing model couldn't keep up",
        "what": "Zillow Offers used an algorithm to buy and flip homes at scale. When the market "
                "shifted, the model's forecasts went wrong, and Zillow shut the unit down after "
                "roughly half a billion dollars in losses.",
        "lesson": "Data drift is expensive: a model tuned to yesterday's market fails when the "
                  "world moves.",
        "epic": "Model / Govern (drift)",
        "link": "https://www.wsj.com/articles/zillow-quits-home-flipping-business-cites-inability-"
                "to-forecast-prices-11635883500",
    },
    {
        "company": "Amazon",
        "icon": "📦",
        "title": "The recruiting AI that learned to prefer men",
        "what": "Amazon trained a hiring model on ten years of résumés — mostly from men — so it "
                "penalised CVs mentioning 'women's'. The tool was scrapped before wide use.",
        "lesson": "A model learns the bias in its training data. Biased inputs → biased "
                  "decisions, at scale.",
        "epic": "Judgment / Govern (fairness)",
        "link": "https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-"
                "idUSKCN1MK08G",
    },
    {
        "company": "ProPublica / COMPAS",
        "icon": "⚖️",
        "title": "Biased risk scores in criminal sentencing",
        "what": "An investigation found a widely-used recidivism-risk algorithm flagged Black "
                "defendants as high-risk far more often, with more false positives, than white "
                "defendants.",
        "lesson": "‘The algorithm decided’ is not neutral — unaudited models can encode and "
                  "amplify discrimination.",
        "epic": "Govern (fairness) / Judgment",
        "link": "https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-"
                "sentencing",
    },
    {
        "company": "Netflix",
        "icon": "🎬",
        "title": "Recommendations that drive most of what's watched",
        "what": "Netflix has said personalised recommendations influence the large majority of "
                "what members choose to watch, and are worth an estimated $1B+ a year in "
                "retention.",
        "lesson": "A good recommender isn't a gimmick — it's a core revenue engine.",
        "epic": "Model (recommend) / Mine",
        "link": "https://www.wired.com/2013/08/qq-netflix-algorithm/",
    },
    {
        "company": "Cambridge Analytica",
        "icon": "🗳️",
        "title": "Harvested data and political targeting",
        "what": "Data on tens of millions of Facebook users was harvested without meaningful "
                "consent and used to build political-targeting profiles — a global scandal that "
                "reshaped data-privacy law.",
        "lesson": "How you *collect* data is a decision with legal and ethical weight, not a "
                  "technical afterthought.",
        "epic": "Collect / Govern (PII)",
        "link": "https://www.theguardian.com/news/2018/mar/17/cambridge-analytica-facebook-"
                "influence-us-election",
    },
]


def cases() -> list[dict]:
    return list(CASES)


def companies() -> list[str]:
    return [c["company"] for c in CASES]
