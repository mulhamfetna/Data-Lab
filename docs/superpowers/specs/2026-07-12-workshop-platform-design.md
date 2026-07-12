# Data to Decisions — Interactive Workshop Platform — Design Spec

**Date:** 2026-07-12
**Author:** Eng. Mulham Fetna — Neurobotics Academy
**Context:** Turn the "From Data to Decisions" 4-hour workshop (`workshop.md`, audience = senior
non-programmers) into one interactive platform: the slides and a suite of live demos across the
whole data lifecycle, in a single app. Extends the already-built contact scraper, which folds in
as one demo.

---

## 1. Purpose & audience

A single **Streamlit multipage app** that a facilitator drives on a projector. Every page is either
a **slide** (native, with the deck's Mermaid diagrams and a live poll) or a **demo** (a runnable,
interactive illustration of one stage of the data lifecycle).

Audience is **non-programmers** — founders, PMs, clinicians, academics, officials. Every demo is
framed "what this means for a decision-maker," never "here is a coding tutorial." Each demo page
carries a one-line **📎 Leader takeaway**.

### Success criteria
- One app, one URL, one sidebar: slides + all demos in the same nav.
- The lifecycle demos all operate on **one shared story dataset**, so the audience follows a single
  business from raw mess to decision.
- Every demo runs live in seconds, offline where possible, and degrades gracefully if a network
  call fails on stage.
- Nothing is faked: where real practice uses heavy models (GANs, transformers), the demo shows the
  true *principle* at runnable scale and the talk-track names the real tools. No "AI trained in 5s."

### Non-goals (YAGNI)
- No user accounts, no persistence beyond a local SQLite the Engineer demo writes.
- No training of real deep-learning models live.
- No cloud deploy in this spec (local `streamlit run`).

---

## 2. Architecture

```
workshop-platform/
  Home.py                       # welcome, how-to, the lifecycle map
  pages/
    01_📊_Why_Data.py           # slide page
    02_📊_The_Lifecycle.py      # slide page
    10_🧪_Collect_Scraper.py    # existing scraper, folded in
    11_🧪_Collect_API.py
    12_🧪_Collect_Synthetic.py
    13_🧪_Collect_Datasets.py
    20_🧪_Clean.py
    21_🧪_Filter.py
    22_🧪_Analyze.py
    23_🧪_Engineer.py
    24_🧪_Predict.py
  workshop/
    __init__.py
    store_data.py               # THE shared story dataset (seeded, messy + clean)
    synth.py                    # synthetic generation + validation (used by demo 12)
    ui.py                       # shared header, "📎 Leader takeaway", section styling
  contact_scraper/              # the existing scraper package, moved in unchanged
  assets/                       # bundled datasets (Gapminder csv), preview images
  tests/
  data/                         # SQLite output (gitignored)
  requirements.txt  README.md
```

Streamlit's `pages/` convention gives the sidebar nav for free; numeric prefixes order it. Each page
is **self-contained and independently runnable** (`streamlit run pages/12_..._Synthetic.py` works),
importing only the `workshop/` shared modules — so demos are built and verified independently, and
"grouping" at the end is just dropping the scraper page in + polishing the nav.

### Shared modules (built once, first)
- **`store_data.py`** — `messy_orders(seed=42, n=...) -> DataFrame` and `clean_orders(df) -> DataFrame`.
  The single source of the story data. Seeded, deterministic. Deliberate defects baked in (see §3).
- **`ui.py`** — `page_header(title, takeaway)`, `leader_takeaway(text)`, consistent look; keeps every
  page visually one platform.
- **`synth.py`** — tabular synthetic generation + validation used by the Synthetic demo (§5).

---

## 3. The shared story — "Nour Store"

A fictional Syrian online shop. Three related tables the demos share:

- **customers**: customer_id, name, city (Aleppo/Damascus/Homs/Latakia/…), signup_date, age, phone
- **products**: product_id, name, category, unit_price
- **orders**: order_id, customer_id, product_id, quantity, order_date, status, amount

`messy_orders()` bakes in realistic defects so Clean has real work: missing values, duplicate rows,
mixed date formats (`2026-01-05` vs `05/01/2026`), inconsistent city casing/spelling, a few price
outliers, whitespace in names. `clean_orders()` is the reference fix. Everything is seeded and
deterministic so the demo is identical every run.

The story flows: **Synthetic generates it → Clean fixes it → Filter slices it → Analyze decides on it
→ Engineer pipelines it → Predict models it.** The Collect demos (Scraper, API, Datasets) show *other*
real sources feeding the same kind of business.

---

## 4. Shared UI & honesty conventions

- Each demo page: `page_header(title, takeaway)` then the interactive body.
- **📎 Leader takeaway** — one plain-language sentence per demo ("what a decision-maker takes away").
- **Honesty rule (applies to every demo):** never present a simulated result as a real trained model
  or real private data. Where the real world uses heavy ML, show the principle at runnable scale and
  name the real tools in the takeaway/talk-track.

---

## 5. The demo lineup

### Collection

**10 · Scraper** ✅ — the existing contact scraper, folded in as a page. Hook: "your data can come
from any website."

**11 · REST API** — Hook: "live data, from anywhere, instantly." Pull **live currency rates** from a
no-key API (`frankfurter.app` or `open.er-api.com`), show USD/EUR/TRY on screen, one call. Ties to the
store (pricing). Graceful offline fallback: a cached last-response bundled as JSON.

**12 · Synthetic** — the deep one (§5.1).

**13 · Datasets** — Hook: "millions of free datasets already exist." Load a bundled famous dataset
(Gapminder) → instant chart (life expectancy vs income). No network.

### Transform (all on Nour Store's data)

**20 · Clean** — Hook: "why 80% of the work is here." Checkboxes for each fix (dupes, dates, cities,
missing, outliers) → live messy→clean before/after with a row/issue counter.

**21 · Filter** — Hook: "asking questions of data." City + date-range + status controls → table +
totals update live. Shows filtering ≠ deleting.

**22 · Analyze** — Hook: "turning rows into a decision." Revenue by product & city, a monthly trend
chart, and a headline answer ("stock more X in Aleppo").

**23 · Engineer** — Hook: "moving data reliably at scale." Join customers+orders+products → one
analytics table → write to a real **SQLite** file in `data/`; show the pipeline as ordered steps and
let the user re-run it. Teaches "a pipeline is repeatable, not a one-off."

**24 · Predict** — Hook: "train an AI in 90 seconds" (the workshop's slide-4 moment). Train a small,
honest **scikit-learn** model on the store data (predict churn or high-value customer) → user tweaks a
customer's inputs → live prediction + which features drove it. Honest: it's a real (small) model on
synthetic data; takeaway names where real teams go from here.

### 5.1 Synthetic demo (demo 12) — two tabs

Built around the two real motivations, with one shared **generate → validate** mechanic.

**Tab 1 — "Not enough data" (augmentation).** Story hooks in the talk-track: drug-interaction research
(predict unreported interactions from reported cases + cohort DNA/history), breast-cancer imaging (too
few labelled scans to feed a transformer), and the software-house/animal-farm case (no real data yet —
synthesize from a schema to stress-test edge cases; this is also what produces the Nour Store set).
Live mechanic: from a small real seed, generate N synthetic rows.

**Tab 2 — "Can't use the real data" (privacy).** Story hook: EU hospital data can't leave the EU / is
GDPR-restricted; generate a synthetic twin that matches the statistics but contains no real person —
"real in scientific context, belongs to no one."

**The validation loop (both tabs, the honest core):**
1. **Generate** synthetic rows from the seed (per-column distribution sampling preserving correlations
   — real, runnable; *not* a GAN).
2. **Validate — utility:** overlay real vs synthetic distributions + a correlation comparison → "it
   behaves like the real population."
3. **Validate — privacy/trust:** nearest-neighbour distance from each synthetic row to the real rows →
   "it matches the population, not any individual; no real record leaked."

**Honesty boundary:** the demo does statistical generation + validation (what tabular tools like SDV
actually do). It explicitly does **not** train a GAN/VAE/diffusion/transformer live; the talk-track
names those as what medical-imaging and DNA teams use at scale, running the *same* generate→validate
principle shown on screen.

---

## 6. Slides pages

Native Streamlit pages rebuilding the deck's key segments: **Why Data** and **The Lifecycle** first
(text + the deck's Mermaid diagrams via `st.graphviz_chart`/image + one live audience poll widget).
More segments portable later. This is what makes it "one platform," not an app beside a PDF.

---

## 7. Build sequence (independent now, grouped at end)

1. **Foundation:** `workshop/store_data.py`, `workshop/ui.py`, `Home.py`, app shell. Verifiable: app
   runs, Home renders, `store_data` unit-tested.
2. **Synthetic demo (12)** — establishes the pattern and the story data; both tabs + validation.
3. **Lifecycle demos** on the shared data: Clean → Filter → Analyze → Engineer → Predict.
4. **Collection demos:** REST API, Datasets (independent).
5. **Slides pages:** Why Data, The Lifecycle.
6. **Integrate:** move the scraper package in as page 10; final nav/polish.

Each step ships an independently runnable page. This spec is the whole vision; each step gets its own
implementation plan.

---

## 8. Testing

- **Pure logic is unit-tested offline:** `store_data` (defects present in messy, gone in clean, seeded
  determinism), `synth` (generation shape, validation metrics, privacy nearest-neighbour), each demo's
  data-transform helpers, cleaning functions, the SQLite engineer step, the model-training helper
  (fits, predicts, deterministic with a seed).
- **UI pages** get a Streamlit `AppTest` smoke (loads, no exception) with any network patched.
- Network demos (API) have a bundled cached response so tests and the stage never depend on the wire.

---

## 9. Dependencies

`streamlit`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`/`altair`, `requests`, `openpyxl`
(reused from the scraper), `pytest`. All already present in the environment. SQLite via stdlib.
The scraper's own deps (beautifulsoup4, pillow, playwright) come with it when folded in.
