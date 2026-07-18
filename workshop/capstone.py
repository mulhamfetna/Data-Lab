"""Capstone — walk one scenario through the whole data lifecycle, and get scored.

Every demo teaches one stage in isolation. The capstone stitches them into a single story:
you are leading Nour Store's data initiative, and at each stage you make the call a leader
actually makes — what to collect, whether to trust the data, which metric to believe, when
to ship the model. Your score is how many good decisions you made, with the reasoning shown.
"""
from __future__ import annotations

# Each step mirrors one lifecycle stage. best = index of the strongest leadership choice.
STEPS: list[dict] = [
    {
        "stage": "Collect",
        "question": "You want to know why customers churn. What's the best first move?",
        "options": [
            "Buy a huge external dataset of consumer profiles",
            "Start from the order and support data you already own",
            "Launch a brand-new AI model immediately",
        ],
        "best": 1,
        "why": "Your own first-party data is cheaper, cleaner-to-consent, and directly relevant. "
               "Start there before buying anything.",
    },
    {
        "stage": "Clean",
        "question": "The city column has 'Aleppo', 'aleppo', and ' ALEPPO '. What do you do?",
        "options": [
            "Ignore it — close enough",
            "Standardise them to one value before any analysis",
            "Delete every row that isn't perfectly formatted",
        ],
        "best": 1,
        "why": "Inconsistent categories silently split your totals. Standardise; don't delete "
               "real data over formatting.",
    },
    {
        "stage": "Analyze",
        "question": "A report shows sales up 4%, drawn as a chart that looks like it doubled. "
                    "Your reaction?",
        "options": [
            "Celebrate the huge jump",
            "Check the axis — the visual may be exaggerating a small change",
            "Ask to cut the price further",
        ],
        "best": 1,
        "why": "A truncated axis turns 4% into a rocket. Always read the numbers, not just the "
               "shape.",
    },
    {
        "stage": "Predict",
        "question": "A model flags 'high-value' customers at 92% accuracy. Before you act on it?",
        "options": [
            "Deploy it everywhere — 92% is great",
            "Ask what drives it and whether the accuracy is real or built-in",
            "Replace all human judgement with it",
        ],
        "best": 1,
        "why": "High accuracy can be an artefact of how the label was made. Ask for feature "
               "attribution and an honest test before trusting it.",
    },
    {
        "stage": "Decide",
        "question": "The AI answers a policy question with a confident but unsourced claim. "
                    "You should?",
        "options": [
            "Trust it — it sounded certain",
            "Require it to cite the source document, or say 'I don't know'",
            "Forward it to customers as-is",
        ],
        "best": 1,
        "why": "Confidence is not correctness. Ground answers in trusted sources and demand a "
               "citation — that's the guardrail against hallucination.",
    },
]


def grade(answers: dict[int, int]) -> dict:
    """Score chosen answers (step index → option index). Returns score, max, per-step results."""
    results = []
    score = 0
    for i, step in enumerate(STEPS):
        chosen = answers.get(i)
        correct = chosen == step["best"]
        score += int(correct)
        results.append({"stage": step["stage"], "correct": correct,
                        "chosen": chosen, "best": step["best"], "why": step["why"]})
    return {"score": score, "max": len(STEPS), "results": results}


def verdict(score: int, total: int) -> str:
    """A short leadership-flavoured verdict for a final score."""
    ratio = score / total if total else 0
    if ratio == 1:
        return "Data-fluent leader — you'd catch the traps and ask the right questions."
    if ratio >= 0.6:
        return "Solid instincts — a few traps slipped through; revisit those stages."
    return "Worth another pass — the demos for the missed stages will sharpen these calls."
