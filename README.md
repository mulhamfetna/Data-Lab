# 📊 Data to Decisions — Interactive Data-Literacy Workshop Platform

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Built with Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b.svg)](https://streamlit.io/)
[![DOI](https://zenodo.org/badge/1304803192.svg)](https://zenodo.org/badge/latestdoi/1304803192)

A multi-page [Streamlit](https://streamlit.io/) app that teaches **non-programmers** the full
data lifecycle as **live, hands-on demos** — one URL, slides and demos in the same sidebar. It is
the interactive backbone of the *From Data to Decisions* workshop by **Neurobotics Academy**
(Eng. Mulham Fetna).

Every demo follows one small fictional business — *Nour Store* — from raw, messy data all the way
to a decision, so the audience watches a single story become a decision.

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

The roadmap of upcoming **Data Lab** modules (mining, big data, labeling, tokenization,
quantization, governance, and more) is tracked in the repository's GitHub Issues.

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

## Citation

If you use this platform, please cite it — see [`CITATION.cff`](CITATION.cff). GitHub renders a
**"Cite this repository"** button from that file.

## License

[AGPL-3.0-or-later](LICENSE) © 2026 Mulham Fetna / Neurobotics Academy.
