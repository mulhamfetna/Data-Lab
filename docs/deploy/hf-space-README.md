---
title: Data Lab
emoji: 🧪
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
license: agpl-3.0
short_description: Free hands-on data-literacy lab for non-coders (EN / العربية)
---

# 📊 Data-Lab — From Data to Decisions

A **free, hands-on data-literacy lab** for people who **decide with data but don't code** —
in English and Arabic. Touch real data, watch a wrong conclusion form, and learn the judgment
behind every chart, model, and AI answer.

68 hands-on demos across the whole data lifecycle: collecting, cleaning, analysing, modelling,
data judgment (Simpson's paradox, sampling bias, p-hacking), GenAI (RAG, guardrails,
hallucination), explainability, and advanced analytics.

- 🌐 **Website:** <https://datalab.mulhamfetna.com>
- 💻 **Source:** <https://github.com/mulhamfetna/Data-Lab>
- 📄 **Licence:** AGPL-3.0 · **DOI:** [10.5281/zenodo.21427808](https://doi.org/10.5281/zenodo.21427808)
- 👤 By **Eng. Mulham Fetna** — Neurobotics Academy

## AI features in this Space

The GenAI demos run live on **Hugging Face Inference Providers** when an `HF_TOKEN` secret is
set on the Space (Settings → Variables and secrets). The app auto-detects it and prefers
Hugging Face inference while running here.

Default model: `openai/gpt-oss-20b:cheapest` — open-weights (no licence gating), served by
several providers, and routed to the lowest cost per output token to stretch the free monthly
quota. Override with an `LLM_MODEL` variable.

**Without a token the app still works fully** — the GenAI demos fall back to a clearly-labelled
offline simulation. A simulation is never presented as a real model.

> Note: the web-scraper demo's Syrian (`.sy`) targets are geo-restricted and unreachable from
> cloud hosts; run the app locally on a Syrian connection for those. Everything else works here.

---

*This file is the Space's README. It is published automatically from
`docs/deploy/hf-space-README.md` in the GitHub repo by the `sync-to-hf-space` workflow — edit it
there, not on the Space.*
