# Contributing to Data-Lab

Thanks for your interest! This project is built with a strict, simple workflow.

## Workflow

1. **One issue per change.** Pick or open an issue.
2. **Branch:** `git checkout -b feat/<issue>-<slug>` off `main`.
3. **Test-first:** add tests in `tests/`, then the code.
4. **Structure:** pure logic goes in `workshop/` (no Streamlit imports except `ui.py`);
   Streamlit pages go in `pages/` as thin views over that logic.
5. **Run the suite:** `python3 -m pytest -m "not live"` — it must pass, and coverage must stay
   ≥ 90% (`--cov=workshop --cov-fail-under=90`).
6. **Open a PR to `main`** with `Closes #<issue>`. CI runs automatically and must pass.
7. **Squash-merge.** `main` is protected: PR required, CI required.

## Conventions

- Every demo page ends with a `📎 Leader takeaway` via `workshop.ui.leader_takeaway`.
- Charts use the shared palette in `workshop/visuals.py` (colourblind-safe).
- **Honesty rule:** never present a simulated result as a real trained model, live GAN, Spark
  cluster, or private data. Show the true principle at runnable scale and name the real tools.
- Keep the app **offline-safe**: no external images or required network calls on page load.

## Local setup

```bash
pip install -r requirements.txt
./run.sh                       # launch the app
python3 -m pytest -m "not live"  # run tests
```
