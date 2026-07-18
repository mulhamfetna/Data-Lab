"""Role-based tracks — a curated path through the lab for who you actually are.

Eighty demos is a lot. A founder, a clinician, and a product manager each care about a
different slice. These tracks are short, opinionated playlists — the handful of demos most
relevant to each role, in a sensible order, with a one-line reason each. It turns "explore
everything" into "here's your 30 minutes."
"""
from __future__ import annotations

TRACKS: dict[str, dict] = {
    "Founder / CEO": {
        "icon": "💼",
        "blurb": "Where data turns into money and risk — value, prediction, and the big calls.",
        "demos": [
            ("pages/11_🧪_Collect_API.py", "Live API", "Where real-time data comes from."),
            ("pages/12_🧪_Collect_Synthetic.py", "Synthetic data",
             "Move fast when you don't have enough real data."),
            ("pages/24_🧪_Predict.py", "Predict", "A real model spotting high-value customers."),
            ("pages/94_🧪_Adv_Optimize.py", "Optimization",
             "The price that maximises profit, not sales."),
            ("pages/95_🧪_Adv_MonteCarlo.py", "Monte Carlo",
             "See the range and the risk, not one fragile forecast."),
            ("pages/99_🎓_Capstone.py", "Capstone", "Test your judgement across the lifecycle."),
        ],
    },
    "Clinician / Researcher": {
        "icon": "🔬",
        "blurb": "Trust, privacy, and not being fooled — the stakes are high in your field.",
        "demos": [
            ("pages/12_🧪_Collect_Synthetic.py", "Synthetic data",
             "Augment scarce data and protect patient privacy."),
            ("pages/69_🧪_Govern_PII.py", "PII masking", "Keep identifiers out of the analysis."),
            ("pages/83_🧪_Judgment_Sampling.py", "Sampling bias",
             "Why the wrong sample gives the wrong answer."),
            ("pages/82_🧪_Judgment_Causation.py", "Correlation vs causation",
             "The confounder trap, in one chart."),
            ("pages/70_🧪_Govern_Fairness.py", "Fairness audit",
             "Check a model isn't biased across groups."),
            ("pages/91_🧪_GenAI_Guardrails.py", "Guardrails",
             "Why AI invents facts — and how to fence it."),
        ],
    },
    "Product Manager": {
        "icon": "📦",
        "blurb": "Metrics you'll defend and features you'll ship — evidence over opinion.",
        "demos": [
            ("pages/22_🧪_Analyze.py", "Analyze", "Turn raw orders into the numbers you report."),
            ("pages/62_🧪_Model_ABTest.py", "A/B testing",
             "Prove a change worked before you roll it out."),
            ("pages/98_🧪_Adv_Recommender.py", "Recommender",
             "The 'you might also like' engine, explained."),
            ("pages/90_🧪_GenAI_Classify.py", "Zero-shot classifier",
             "Auto-route feedback with no training data."),
            ("pages/71_🧪_Govern_Drift.py", "Data drift",
             "Why a good model quietly goes stale."),
            ("pages/87_🧪_GenAI_RAG.py", "RAG", "Chat-with-your-docs, and when to trust it."),
        ],
    },
    "Consultant / Analyst": {
        "icon": "📈",
        "blurb": "The craft: clean data, honest charts, and traps you must never miss.",
        "demos": [
            ("pages/20_🧪_Clean.py", "Clean", "The unglamorous 80% of every real project."),
            ("pages/42_🧪_Acquire_SQL.py", "SQL extraction", "Pull exactly the slice you need."),
            ("pages/81_🧪_Judgment_Simpson.py", "Simpson's paradox",
             "The trend that flips when you group it."),
            ("pages/84_🧪_Judgment_Charts.py", "Misleading charts",
             "Same numbers, opposite impression."),
            ("pages/85_🧪_Judgment_Stats.py", "CIs & p-hacking",
             "When 'significant' means nothing."),
            ("pages/92_🧪_XAI_Attribution.py", "Feature attribution",
             "Prove what a model actually uses."),
        ],
    },
}


def roles() -> list[str]:
    return list(TRACKS)


def track(role: str) -> dict:
    return TRACKS[role]


def all_demo_files() -> list[str]:
    """Every page file referenced by any track — used to validate the links stay live."""
    return [d[0] for t in TRACKS.values() for d in t["demos"]]
