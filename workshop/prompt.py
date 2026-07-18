"""Prompt engineering playground — how the *way you ask* steers an LLM's answer.

Offline we can't run a model, but we can teach the anatomy of a good prompt: given a
task, build four prompts from vague to well-engineered and score each against a rubric
of the five things a strong prompt usually has. With a key, the page additionally sends
each variant to Claude so the audience sees the answers actually change.
"""
from __future__ import annotations

import re

# Each rubric item: (key, human label, a regex that hints the element is present).
RUBRIC: list[tuple[str, str, str]] = [
    ("task", "States the task clearly",
     r"\b(summar|classif|extract|write|list|explain|translate|draft|compare)\w*"),
    ("context", "Gives context / background",
     r"\b(context|background|the following|below|our|company|customer|based on)\b"),
    ("format", "Specifies the output format",
     r"\b(bullet|list|table|json|one sentence|paragraph|steps|columns?)\b"),
    ("constraints", "Adds constraints (length, tone, audience)",
     r"\b(exactly|at most|no more than|words?|tone|formal|simple|for a|audience|non-?technical)\b"),
    ("persona", "Sets a role / persona",
     r"\b(you are|act as|as an? |expert|analyst|assistant|specialist)\b"),
]


def build_variants(task: str) -> dict[str, str]:
    """Four prompts for the same *task*, from throwaway to engineered."""
    task = task.strip().rstrip(".")
    return {
        "vague": task,
        "specific": f"{task}. Be accurate and concise.",
        "formatted": (f"{task}. Answer as exactly 3 short bullet points, "
                      "each under 15 words."),
        "engineered": (
            "You are a helpful business analyst writing for a non-technical manager. "
            f"Task: {task}. Use the context provided by the user. "
            "Answer as exactly 3 short bullet points, each under 15 words, in plain language."),
    }


def score_prompt(prompt: str) -> dict:
    """Detect which rubric elements a prompt contains; return hits + score out of 5."""
    low = prompt.lower()
    hits = {key: bool(re.search(pat, low)) for key, _label, pat in RUBRIC}
    return {"hits": hits, "score": sum(hits.values()), "max": len(RUBRIC)}


def label_for(key: str) -> str:
    return next(lbl for k, lbl, _ in RUBRIC if k == key)
