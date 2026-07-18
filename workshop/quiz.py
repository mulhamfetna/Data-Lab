"""Quizzes per epic — quick knowledge checks that make the lessons stick.

A demo you watch fades; a question you answer sticks. Each epic gets two or three
plain-language checks — no code, just the judgement the epic was teaching — with instant
feedback and the reason for the right answer. Facilitators use them as segment recaps.
"""
from __future__ import annotations

QUIZZES: dict[str, list[dict]] = {
    "Collect": [
        {"q": "Why prefer your own (first-party) data before buying external data?",
         "options": ["It's always bigger", "It's cheaper, relevant, and consent is clearer",
                     "External data is illegal"],
         "best": 1,
         "why": "First-party data is directly relevant and you control its consent and quality."},
        {"q": "Synthetic data is most useful when…",
         "options": ["You want to fake results",
                     "You lack enough real data or must protect privacy",
                     "You never need real data again"],
         "best": 1,
         "why": "It fills gaps and protects privacy — it doesn't replace validating on real data."},
    ],
    "Clean": [
        {"q": "'Aleppo', 'aleppo', ' ALEPPO ' in one column will…",
         "options": ["Not matter", "Silently split your totals across three 'cities'",
                     "Improve accuracy"],
         "best": 1,
         "why": "Inconsistent categories fragment aggregates — standardise before analysing."},
        {"q": "A missing value is best handled by…",
         "options": ["Always deleting the row", "Understanding why it's missing, then imputing "
                     "or excluding deliberately", "Filling it with zero always"],
         "best": 1,
         "why": "The reason it's missing decides the fix; blind deletion or zero-fill distorts."},
    ],
    "Analyze": [
        {"q": "A chart makes a 4% rise look enormous. The likely cause?",
         "options": ["Sales really doubled", "A truncated axis exaggerating the change",
                     "Too much data"],
         "best": 1,
         "why": "Cropping the y-axis turns a small change into a dramatic-looking one."},
        {"q": "Ice-cream sales and drownings both rise together. This means…",
         "options": ["Ice cream causes drowning", "A hidden factor (summer heat) drives both",
                     "Drowning causes ice-cream sales"],
         "best": 1,
         "why": "Correlation isn't causation — look for the confounder before concluding."},
    ],
    "Predict": [
        {"q": "A model reports 92% accuracy. Before trusting it you should…",
         "options": ["Deploy immediately", "Ask what drives it and whether accuracy is real "
                     "or built-in", "Fire the analysts"],
         "best": 1,
         "why": "Accuracy can be an artefact of how the label was defined — check attribution."},
        {"q": "Feature attribution tells you…",
         "options": ["How fast the model runs", "Which inputs actually drive the decisions",
                     "The price of the model"],
         "best": 1,
         "why": "It reveals what the model leans on — and whether it's the wrong thing."},
    ],
    "Judgment": [
        {"q": "Simpson's paradox is when…",
         "options": ["Data is missing", "A trend reverses once you split into subgroups",
                     "A model overfits"],
         "best": 1,
         "why": "An aggregate can point the opposite way to every subgroup within it."},
        {"q": "Testing 20 things and reporting the one 'significant' result is…",
         "options": ["Good practice", "p-hacking — that result is likely noise",
                     "Impossible"],
         "best": 1,
         "why": "At p<0.05, roughly 1 in 20 pure-noise tests 'wins' by chance."},
    ],
    "GenAI": [
        {"q": "An LLM gives a confident answer with no source. You should…",
         "options": ["Trust it — it sounded sure", "Require a citation or an 'I don't know'",
                     "Publish it to customers"],
         "best": 1,
         "why": "Confidence isn't correctness; grounding + citations fence off hallucination."},
        {"q": "RAG (retrieval-augmented generation) mainly helps by…",
         "options": ["Making the model bigger", "Grounding answers in your own documents",
                     "Removing the need for data"],
         "best": 1,
         "why": "It retrieves your relevant text so the model answers from your facts."},
    ],
}


def epics() -> list[str]:
    return list(QUIZZES)


def grade_quiz(epic: str, answers: dict[int, int]) -> dict:
    """Score answers (question index → option index) for one epic's quiz."""
    questions = QUIZZES[epic]
    results, score = [], 0
    for i, item in enumerate(questions):
        correct = answers.get(i) == item["best"]
        score += int(correct)
        results.append({"correct": correct, "best": item["best"], "why": item["why"]})
    return {"score": score, "max": len(questions), "results": results}
