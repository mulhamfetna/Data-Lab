"""The facilitator agenda: segments, time budgets, and talk-track cues (from workshop.md)."""

SEGMENTS = [
    {"title": "Open / Hook", "min": 15, "note": "Word-cloud poll; set the promise: sharper questions, not coding."},
    {"title": "Decision Making — role of data", "min": 25, "note": "Target story; gut vs data rater."},
    {"title": "Data Lifecycle", "min": 25, "note": "Collect→Report; 80% is the unglamorous middle."},
    {"title": "☕ Break", "min": 10, "note": "Countdown timer."},
    {"title": "The 7 Data Sources", "min": 28, "note": "'What gold are you sitting on?' mapping."},
    {"title": "Data Tools + Train an AI", "min": 30, "note": "Predict demo; the 90-second AI moment."},
    {"title": "☕ Mid break + networking", "min": 15, "note": "Warm intros."},
    {"title": "Learning Roadmap", "min": 28, "note": "8 phases + anti-hype filter."},
    {"title": "Tech Roles", "min": 22, "note": "Who to hire; Zillow story."},
    {"title": "Career Growth", "min": 22, "note": "Proof beats certificates; Amazon story."},
    {"title": "Close — 3 actions + Q&A", "min": 20, "note": "Callback to the opening word."},
]


def total_minutes() -> int:
    return sum(s["min"] for s in SEGMENTS)
