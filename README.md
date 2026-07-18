# 📊 Data to Decisions — Interactive Data-Literacy Workshop Platform

[![Live site](https://img.shields.io/badge/Live_site-mulhamfetna.github.io%2FData--Lab-0072B2?logo=githubpages&logoColor=white)](https://mulhamfetna.github.io/Data-Lab/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Built with Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b.svg)](https://streamlit.io/)
[![coverage](https://img.shields.io/badge/coverage-%E2%89%A590%25-brightgreen)](.github/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/1304803192.svg)](https://zenodo.org/badge/latestdoi/1304803192)

A multi-page [Streamlit](https://streamlit.io/) app that teaches **non-programmers** the full
data lifecycle as **live, hands-on demos** — one URL, slides and demos in the same sidebar. It is
the interactive backbone of the *From Data to Decisions* workshop by **Neurobotics Academy**
(Eng. Mulham Fetna).

Every demo follows one small fictional business — *Nour Store* — from raw, messy data all the way
to a decision, so the audience watches a single story become a decision.

**🔗 Live site:** <https://mulhamfetna.github.io/Data-Lab/>

## Run

```bash
./run.sh
```

or

```bash
pip install -r requirements.txt
streamlit run Home.py
```

Opens at http://localhost:8501. Override the port with `PORT=9000 ./run.sh`.

## What's inside

**Slides** (native pages): Why Data · The Lifecycle · Learning Roadmap · Tech Roles · Career · Close

**Collect:** Web Scraper · REST API · Synthetic Data · Public Datasets · Internal Data ·
Qualitative→Quantitative · Survey

**Transform (on the shared Nour Store data):** Clean · Filter · Analyze · Engineer
(star schema → SQLite) · Predict (a scikit-learn classifier) · Report

**Data Lab (35 modules across 9 lifecycle stages):**

- **Acquire** — streaming, file formats, SQL extraction, data integration
- **Label** — interactive labeling, active learning, weak supervision
- **Clean** — profiling, deduplication, imputation, outlier treatment
- **Encode** — tokenization, quantization, embeddings, categorical encoding, scaling
- **Mine** — market-basket, clustering/segmentation, anomaly detection
- **Model** — forecasting, recommendation, A/B testing, sentiment, image classification
- **Scale** — big-data chunking, compression, indexing, warehouse-vs-lake
- **Govern** — PII masking, fairness audit, data drift, lineage
- **Serve** — model-as-API, monitoring/retraining, orchestration

**Second wave — judgment, GenAI, and teaching layers:**

- **Data Judgment** — Simpson's paradox, correlation vs causation, sampling bias, misleading
  charts, confidence intervals & p-hacking
- **GenAI / LLM** — prompt playground, RAG, summarization, structured extraction, zero-shot
  classifier, guardrails & hallucination. Each has a **free-provider live path** (Groq /
  OpenRouter / Hugging Face / local Ollama, via their OpenAI-compatible endpoints) and an
  honest offline simulation, so it runs on stage with no key.
- **Explainability (XAI)** — global feature attribution, single-prediction explanation
- **Advanced Analytics** — price optimization, Monte Carlo, geospatial, network analysis,
  matrix-factorization recommender
- **Teaching Layers** — capstone path, role-based tracks, per-epic quizzes, bilingual glossary,
  case-study cards

Every module was built on its own branch and merged via pull request; see the repository's
closed Issues and Releases for the full history.

## Architecture

- `workshop/` — pure, UI-free, unit-tested logic (`store_data`, `cleaning`, `queries`,
  `pipeline`, `model`, `synth`, `sources`, `report`, `visuals`, `live_api`); the one exception is
  `ui.py`, the shared Streamlit header helper.
- `pages/` — thin Streamlit views over that logic (Streamlit's multipage convention).
- `contact_scraper/` — the bundled contact-scraper package powering the Scraper demo.
- `assets/` — bundled datasets and preview images (self-contained, offline-safe).
- `tests/` — pytest suite for the logic modules plus `AppTest` smokes for every page.

## Test

```bash
python3 -m pytest -m "not live"    # offline suite
python3 -m pytest -m live          # network smoke tests
```

## Honest limitations

- **Visuals are generated, not photographed** — matplotlib figures, graphviz diagrams, and inline
  SVG — so the app runs fully offline; it does not embed external stock images.
- The **Predict** demo trains a small, real model on synthetic data; its "high-value" label is
  spend-derived, so accuracy is high partly by construction — it illustrates the idea, it is not a
  hard predictive benchmark.
- The **Synthetic** demo does real statistical generation + validation; it does **not** train a
  GAN/transformer live, and says so — it shows the principle those methods scale up.
- The **Scraper** demo's Syrian (`.sy`) targets are geo-restricted and only reachable from within
  Syria; scraping runs server-side, so run the app locally on a Syrian connection for those.
- The **GenAI** demos call a real model only when a free provider key is set (`GROQ_API_KEY`,
  `OPENROUTER_API_KEY`, `HF_TOKEN`, or a local `OLLAMA_HOST`); with none set they run a
  clearly-labeled offline simulation and never present it as a real model.

## Citation

If you use this platform, please cite it. Archived on Zenodo — concept DOI
[10.5281/zenodo.21427808](https://doi.org/10.5281/zenodo.21427808) (always resolves to the
latest version). GitHub also renders a **"Cite this repository"** button from
[`CITATION.cff`](CITATION.cff).

```bibtex
@software{fetna_datalab_2026,
  author    = {Fetna, Mulham},
  title     = {Data to Decisions: An Interactive Data-Literacy Workshop Platform},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21427808},
  url       = {https://github.com/mulhamfetna/Data-Lab}
}
```

## License

[AGPL-3.0-or-later](LICENSE) © 2026 Mulham Fetna / Neurobotics Academy.
