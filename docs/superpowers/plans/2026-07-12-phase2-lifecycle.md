# Phase 2 — Lifecycle Demos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans / subagent-driven-development. Steps use checkbox syntax.

**Goal:** Five demos on the shared Nour Store data — Clean, Filter, Analyze, Engineer, Predict — each a self-contained page over a tested pure-logic helper.

**Architecture:** Pure logic in `workshop/` (no Streamlit): `cleaning.py`, `queries.py`, `pipeline.py`, `model.py`. Pages in `pages/` are thin views. Same TDD + `AppTest` smoke pattern as Phase 1.

## Global Constraints
- `workshop/` stays Streamlit-free (except `ui.py`). Seeded/deterministic. Non-programmer framing + `ui.leader_takeaway` on every page. TDD. Standard commit trailer.

---

### Task 1: `cleaning.py` — composable cleaning steps + issue report
**Files:** Create `workshop/cleaning.py`; Test `tests/test_cleaning.py`.
**Interfaces:** `issues(df) -> dict` (counts: `duplicates`, `missing_amount`, `bad_quantity`, `messy_city`); step fns `dedupe(df)`, `normalize_cities(df)`, `parse_dates(df)`, `fill_amounts(df)`, `drop_bad_quantity(df)`; `apply_steps(df, steps: list[str]) -> df`.

TDD: from `store_data.messy_orders()`, `issues()` reports >0 for each; each step drives its own counter to 0; `apply_steps` with all steps ⇒ matches `store_data.clean_orders` invariants (no dupes, no missing amount, qty>0, cities title-case, dates datetime).

---

### Task 2: `queries.py` — filter + aggregations
**Files:** Create `workshop/queries.py`; Test `tests/test_queries.py`.
**Interfaces:** `filter_orders(df, cities=None, statuses=None, date_from=None, date_to=None, min_amount=None) -> df`; `revenue_by(df, col) -> df` (col→amount sum, sorted desc); `monthly_revenue(df) -> df` (year-month → amount sum).

TDD on `clean_orders(messy_orders())`: filtering by a city returns only that city; date range bounds respected; `revenue_by("product")` sums match a manual groupby and is sorted; `monthly_revenue` returns one row per present month.

---

### Task 3: `pipeline.py` — star schema + SQLite load
**Files:** Create `workshop/pipeline.py`; Test `tests/test_pipeline.py`.
**Interfaces:** `build_star_schema(df) -> dict[str, DataFrame]` (`dim_customer`, `dim_product`, `fact_orders`); `load_to_sqlite(tables: dict, path) -> None`; `table_counts(path) -> dict[str,int]`.

TDD: schema has the three tables; `dim_product` unique on product; `fact_orders` row count == input; round-trip to a tmp SQLite then `table_counts` matches.

---

### Task 4: `model.py` — high-value customer classifier
**Files:** Create `workshop/model.py`; Test `tests/test_model.py`.
**Interfaces:** `build_features(df) -> (X: DataFrame, y: Series)` (per-customer: n_orders, total_qty, avg_amount, top city one-hot; label = total spend ≥ median); `train(X, y, seed=0) -> (model, metrics: dict)` (sklearn LogisticRegression/RandomForest; metrics has `accuracy`); `predict_one(model, features: dict) -> dict` (`label`, `proba`).

TDD: features non-empty, y binary; `train` returns accuracy in [0,1] and is deterministic for a seed; `predict_one` returns a 0/1 label and a probability in [0,1].

---

### Tasks 5-9: the pages (thin views + AppTest smoke each)
- `pages/20_🧪_Clean.py` — checkboxes per fix → `cleaning.apply_steps`; before/after counts + table.
- `pages/21_🧪_Filter.py` — city/status/date/min-amount widgets → `queries.filter_orders`; table + revenue metric.
- `pages/22_🧪_Analyze.py` — `revenue_by` bar charts (product, city) + `monthly_revenue` line + headline insight.
- `pages/23_🧪_Engineer.py` — run `build_star_schema` → `load_to_sqlite` (data/nour.db) → show tables + `table_counts`; re-run button.
- `pages/24_🧪_Predict.py` — `build_features`+`train`, show accuracy + importance; inputs → `predict_one` live.

Each page: `ui.page_header(title, takeaway)`, import only `workshop/` helpers, and a `tests/test_page_*.py` `AppTest` smoke asserting `not at.exception`.

---

## Self-Review
Covers spec §5 transform demos (20-24) + §3 shared data reuse. Pure helpers tested offline; pages get smokes. Types: `filter_orders`/`revenue_by`/`monthly_revenue`, `build_star_schema` keys, `build_features`/`train`/`predict_one` signatures consistent between modules, tests, and pages.
