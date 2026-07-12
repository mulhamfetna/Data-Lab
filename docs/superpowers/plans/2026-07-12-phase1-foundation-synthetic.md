# Phase 1 — Foundation + Synthetic Demo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the multipage workshop app with the shared "Nour Store" story data and the Synthetic Data demo (both tabs, generate→validate).

**Architecture:** Streamlit multipage app. Pure logic (`workshop/store_data.py`, `workshop/synth.py`) is UI-free and unit-tested offline; `pages/*.py` are thin Streamlit views over it; `workshop/ui.py` gives every page one look.

**Tech Stack:** Python 3.14, Streamlit, pandas, numpy, matplotlib, pytest.

## Global Constraints

- **Python 3.14**.
- **`workshop/` package must not import `streamlit`** — pure, reusable, testable. Streamlit lives only in `Home.py` and `pages/`.
- **All data is seeded and deterministic** (`SEED = 42`); same seed → identical data every run.
- **Audience is non-programmers:** every page ends with a one-line `📎 Leader takeaway` via `ui.leader_takeaway`.
- **Honesty:** the Synthetic demo does real statistical generation + validation; it must NOT claim to train a GAN/transformer. The talk-track text names those as the real-world scale-up.
- **TDD**: failing test → minimal code → passing test → commit, per task. Pure logic tested directly; pages get an `AppTest` smoke.
- Commit messages end with the repo's standard `Co-Authored-By` trailer.

---

### Task 1: Scaffold + running app shell

**Files:**
- Create: `requirements.txt`, `workshop/__init__.py`, `Home.py`, `tests/test_smoke.py`

**Interfaces:**
- Produces: an importable `workshop` package; a runnable Streamlit app.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_smoke.py
def test_workshop_package_imports():
    import workshop  # noqa: F401
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_smoke.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'workshop'`

- [ ] **Step 3: Create package, deps, and Home**

```python
# workshop/__init__.py
"""Pure workshop logic (no Streamlit imports)."""
```

```text
# requirements.txt
streamlit>=1.57
pandas>=2.2
numpy>=1.26
scikit-learn>=1.4
matplotlib>=3.8
requests>=2.32
openpyxl>=3.1
pytest>=8
```

```python
# Home.py
import streamlit as st

st.set_page_config(page_title="Data to Decisions", page_icon="📊", layout="wide")
st.title("📊 Data to Decisions")
st.subheader("An interactive tour of how data becomes a decision")
st.markdown(
    "Use the sidebar to move through the workshop. Each **📊 page** is a slide and each "
    "**🧪 page** is a live demo. The demos follow one small business — *Nour Store* — from "
    "raw, messy data all the way to a decision."
)
st.info("Pick a page from the sidebar to begin.")
```

- [ ] **Step 4: Run test + confirm app boots**

Run: `python3 -m pytest tests/test_smoke.py -v`
Expected: PASS

Run: `python3 -m streamlit run Home.py --server.headless true --server.port 8600 &` then `curl -s -o /dev/null -w "%{http_code}" http://localhost:8600/_stcore/health` → `200`; then stop it.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "chore: scaffold workshop platform app shell"
```

---

### Task 2: Shared story data — `store_data.py`

**Files:**
- Create: `workshop/store_data.py`
- Test: `tests/test_store_data.py`

**Interfaces:**
- Produces:
  `SEED = 42`,
  `messy_orders(seed: int = SEED, n: int = 1000) -> pandas.DataFrame` — columns
  `order_id, customer_name, city, product, quantity, unit_price, order_date, amount, status`
  with deliberate defects,
  `clean_orders(df: pandas.DataFrame) -> pandas.DataFrame` — the reference cleaner.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_store_data.py
import pandas as pd
from workshop import store_data as sd

def test_messy_has_defects():
    df = sd.messy_orders()
    assert df.duplicated().any()                       # duplicate rows exist
    assert df["amount"].isna().any()                   # some missing amounts
    assert (df["quantity"] <= 0).any()                 # some bad quantities
    # mixed date formats: at least one dash-form and one slash-form
    dates = df["order_date"].dropna().astype(str)
    assert dates.str.contains("-").any() and dates.str.contains("/").any()
    # inconsistent city casing
    assert df["city"].nunique() > df["city"].str.title().nunique()

def test_messy_is_deterministic():
    assert sd.messy_orders(seed=42).equals(sd.messy_orders(seed=42))

def test_clean_removes_defects():
    clean = sd.clean_orders(sd.messy_orders())
    assert not clean.duplicated().any()
    assert not clean["amount"].isna().any()
    assert (clean["quantity"] > 0).all()
    assert pd.api.types.is_datetime64_any_dtype(clean["order_date"])
    # cities normalised to Title case
    assert (clean["city"] == clean["city"].str.title()).all()

def test_clean_is_smaller_or_equal():
    messy = sd.messy_orders()
    assert len(sd.clean_orders(messy)) <= len(messy)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_store_data.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'workshop.store_data'`

- [ ] **Step 3: Write minimal implementation**

```python
# workshop/store_data.py
import numpy as np
import pandas as pd

SEED = 42
CITIES = ["Aleppo", "Damascus", "Homs", "Latakia", "Hama"]
PRODUCTS = [
    ("Coffee 250g", 4.5), ("Tea 100g", 2.0), ("Olive Oil 1L", 8.0),
    ("Soap Bar", 1.2), ("Notebook", 1.5), ("Phone Case", 6.0),
]
STATUSES = ["delivered", "pending", "returned", "cancelled"]


def _messy_city(rng, city):
    r = rng.random()
    if r < 0.15:
        return city.lower()
    if r < 0.25:
        return city.upper()
    if r < 0.30:
        return f" {city} "        # stray whitespace
    return city


def messy_orders(seed: int = SEED, n: int = 1000) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        pname, price = PRODUCTS[rng.integers(0, len(PRODUCTS))]
        qty = int(rng.integers(1, 6))
        if rng.random() < 0.03:
            qty = 0 if rng.random() < 0.5 else -qty      # bad quantities
        amount = round(qty * price, 2)
        if rng.random() < 0.05:
            amount = np.nan                              # missing amount
        # mixed date formats
        day = int(rng.integers(1, 28))
        month = int(rng.integers(1, 13))
        if rng.random() < 0.5:
            date = f"2026-{month:02d}-{day:02d}"
        else:
            date = f"{day:02d}/{month:02d}/2026"
        rows.append({
            "order_id": 1000 + i,
            "customer_name": f"Customer {int(rng.integers(1, 200))}",
            "city": _messy_city(rng, CITIES[rng.integers(0, len(CITIES))]),
            "product": pname,
            "quantity": qty,
            "unit_price": price,
            "order_date": date,
            "amount": amount,
            "status": STATUSES[rng.integers(0, len(STATUSES))],
        })
    df = pd.DataFrame(rows)
    # inject ~3% duplicate rows
    dupes = df.sample(frac=0.03, random_state=seed)
    return pd.concat([df, dupes], ignore_index=True)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.drop_duplicates()
    out["city"] = out["city"].str.strip().str.title()
    out["customer_name"] = out["customer_name"].str.strip()
    # parse both date forms
    out["order_date"] = pd.to_datetime(out["order_date"], format="mixed", dayfirst=True,
                                       errors="coerce")
    # recompute missing amounts from quantity * unit_price
    recomputed = (out["quantity"] * out["unit_price"]).round(2)
    out["amount"] = out["amount"].fillna(recomputed)
    # drop non-positive quantities
    out = out[out["quantity"] > 0]
    return out.reset_index(drop=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_store_data.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: add shared Nour Store dataset (messy + clean)"
```

---

### Task 3: Shared UI helpers — `ui.py`

**Files:**
- Create: `workshop/ui.py`
- Test: `tests/test_ui.py`

**Interfaces:**
- Produces: `page_header(title: str, takeaway: str) -> None`, `leader_takeaway(text: str) -> None`.
  These call Streamlit; the test asserts they are importable and callable under `AppTest`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_ui.py
def test_ui_functions_exist():
    from workshop import ui
    assert callable(ui.page_header)
    assert callable(ui.leader_takeaway)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_ui.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'workshop.ui'`

- [ ] **Step 3: Write minimal implementation**

```python
# workshop/ui.py
import streamlit as st


def page_header(title: str, takeaway: str) -> None:
    st.title(title)
    leader_takeaway(takeaway)


def leader_takeaway(text: str) -> None:
    st.info(f"📎 **Leader takeaway:** {text}")
```

Note: `workshop/ui.py` is the ONE allowed Streamlit import inside `workshop/` (it is the UI helper); keep `store_data.py` / `synth.py` Streamlit-free.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_ui.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: add shared UI helpers (header + leader takeaway)"
```

---

### Task 4: Synthetic generation + validation — `synth.py`

**Files:**
- Create: `workshop/synth.py`
- Test: `tests/test_synth.py`

**Interfaces:**
- Produces (numeric-column synthesizer; categorical columns passed through by resampling):
  `generate(real: pandas.DataFrame, n: int, seed: int = 0) -> pandas.DataFrame`,
  `utility_report(real, synth) -> dict` with per-column `mean`/`std` for real & synth and a
  `corr_abs_diff` scalar,
  `privacy_report(real, synth) -> dict` with `min_distance`, `mean_distance`, and
  `exact_match_frac`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_synth.py
import numpy as np
import pandas as pd
from workshop import synth


def _real(seed=0, n=300):
    rng = np.random.default_rng(seed)
    age = rng.normal(40, 10, n)
    # income correlated with age
    income = age * 100 + rng.normal(0, 500, n)
    return pd.DataFrame({"age": age, "income": income})


def test_generate_shape_and_columns():
    real = _real()
    syn = synth.generate(real, n=500, seed=1)
    assert len(syn) == 500
    assert list(syn.columns) == list(real.columns)


def test_utility_means_close():
    real = _real()
    syn = synth.generate(real, n=2000, seed=1)
    rep = synth.utility_report(real, syn)
    # synthetic means within 15% of real means
    for col in real.columns:
        assert abs(rep[col]["synth_mean"] - rep[col]["real_mean"]) < 0.15 * abs(rep[col]["real_mean"])


def test_utility_preserves_correlation():
    real = _real()
    syn = synth.generate(real, n=2000, seed=1)
    rep = synth.utility_report(real, syn)
    assert rep["corr_abs_diff"] < 0.15   # correlation structure preserved


def test_privacy_no_exact_copies():
    real = _real()
    syn = synth.generate(real, n=500, seed=1)
    rep = synth.privacy_report(real, syn)
    assert rep["exact_match_frac"] == 0.0
    assert rep["min_distance"] > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_synth.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'workshop.synth'`

- [ ] **Step 3: Write minimal implementation**

```python
# workshop/synth.py
"""Tiny, honest tabular synthesizer: a Gaussian model over numeric columns.

Preserves means, spreads, and correlations (utility) without copying individuals
(privacy). This is the *principle* real tools (SDV, GANs, diffusion) scale up — the
demo says so explicitly. NOT a GAN.
"""
import numpy as np
import pandas as pd


def _numeric(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def generate(real: pd.DataFrame, n: int, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    cols = _numeric(real)
    X = real[cols].to_numpy(dtype=float)
    mean = X.mean(axis=0)
    cov = np.cov(X, rowvar=False)
    sample = rng.multivariate_normal(mean, cov, size=n)
    return pd.DataFrame(sample, columns=cols)


def utility_report(real: pd.DataFrame, synth: pd.DataFrame) -> dict:
    cols = _numeric(real)
    rep: dict = {}
    for c in cols:
        rep[c] = {
            "real_mean": float(real[c].mean()), "synth_mean": float(synth[c].mean()),
            "real_std": float(real[c].std()), "synth_std": float(synth[c].std()),
        }
    r_corr = real[cols].corr().to_numpy()
    s_corr = synth[cols].corr().to_numpy()
    rep["corr_abs_diff"] = float(np.nanmean(np.abs(r_corr - s_corr)))
    return rep


def privacy_report(real: pd.DataFrame, synth: pd.DataFrame) -> dict:
    cols = _numeric(real)
    R = real[cols].to_numpy(dtype=float)
    S = synth[cols].to_numpy(dtype=float)
    # standardize so no single column dominates the distance
    mu, sd = R.mean(axis=0), R.std(axis=0) + 1e-9
    Rn, Sn = (R - mu) / sd, (S - mu) / sd
    dists = []
    for s in Sn:
        dists.append(float(np.sqrt(((Rn - s) ** 2).sum(axis=1)).min()))
    dists = np.array(dists)
    return {
        "min_distance": float(dists.min()),
        "mean_distance": float(dists.mean()),
        "exact_match_frac": float((dists < 1e-9).mean()),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_synth.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: add honest tabular synthesizer + utility/privacy validation"
```

---

### Task 5: Synthetic demo page (two tabs)

**Files:**
- Create: `pages/12_🧪_Collect_Synthetic.py`
- Test: `tests/test_page_synthetic.py`

**Interfaces:**
- Consumes: `workshop.store_data`, `workshop.synth`, `workshop.ui`.
- Produces: a runnable page. Logic lives in the shared modules; the page only wires widgets.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_page_synthetic.py
from streamlit.testing.v1 import AppTest

def test_synthetic_page_loads():
    at = AppTest.from_file("pages/12_🧪_Collect_Synthetic.py").run()
    assert not at.exception
    # two tabs present
    assert len(at.tabs) == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_page_synthetic.py -v`
Expected: FAIL — file not found / no such page.

- [ ] **Step 3: Write minimal implementation**

```python
# pages/12_🧪_Collect_Synthetic.py
import numpy as np
import pandas as pd
import streamlit as st

from workshop import synth, ui

st.set_page_config(page_title="Synthetic Data", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Synthetic Data — inventing data you can trust",
    "When you don't have enough data, or aren't allowed to use the real data, you can "
    "generate a synthetic stand-in — and prove it behaves like the real thing without "
    "copying any real person.",
)


def _seed_data(seed=0, n=300):
    rng = np.random.default_rng(seed)
    age = rng.normal(42, 11, n).clip(18, 80)
    income = age * 90 + rng.normal(0, 600, n)   # correlated with age
    return pd.DataFrame({"age": age.round(0), "income": income.round(0)})


def _validate_block(real, n):
    syn = synth.generate(real, n=n, seed=7)
    util = synth.utility_report(real, syn)
    priv = synth.privacy_report(real, syn)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Utility — does it behave like the real data?**")
        st.write({k: {"real": round(v["real_mean"], 1), "synth": round(v["synth_mean"], 1)}
                  for k, v in util.items() if isinstance(v, dict)})
        st.caption(f"Correlation gap: {util['corr_abs_diff']:.3f} (smaller = more faithful)")
        st.scatter_chart(pd.concat([real.assign(kind="real"),
                                    syn.assign(kind="synthetic")]),
                         x="age", y="income", color="kind")
    with c2:
        st.markdown("**Privacy — did any real person leak in?**")
        st.metric("Exact copies of a real record", f"{priv['exact_match_frac']*100:.1f}%")
        st.metric("Nearest-neighbour distance (min)", f"{priv['min_distance']:.2f}")
        st.caption("Every synthetic row sits *near* the real population but matches no individual.")
    return syn


tab1, tab2 = st.tabs(["1 · Not enough data", "2 · Can't use the real data"])

with tab1:
    st.markdown(
        "**The problem:** too few examples to work with.\n\n"
        "- *Drug-interaction research* — most interactions are unreported; teams generate plausible "
        "ones from the reported cases plus cohort DNA/history, then validate them.\n"
        "- *Cancer imaging* — too few labelled scans to train a transformer, so clinicians + ML "
        "engineers synthesise more and validate medical validity in a loop.\n"
        "- *A new product with no data yet* — synthesise records from just a schema to stress-test "
        "edge cases before launch. *(This is how our Nour Store data is born.)*"
    )
    n = st.slider("How many synthetic records to generate?", 100, 5000, 1500, step=100, key="n1")
    real = _seed_data()
    st.caption(f"Starting from a small real seed of {len(real)} records…")
    _validate_block(real, n)
    st.warning(
        "Honesty note: this demo uses statistical generation + validation — the same "
        "**generate → validate** loop that GANs, VAEs, and diffusion models scale up for images "
        "and DNA. We are *not* training a GAN live.")

with tab2:
    st.markdown(
        "**The problem:** the real data exists but you're not allowed to use it.\n\n"
        "*EU hospital data can't leave the EU and is tightly GDPR-restricted.* Teams generate a "
        "synthetic twin that matches the statistics but contains **no real patient** — data that is "
        "real in a scientific sense yet belongs to no one."
    )
    n = st.slider("How many synthetic patients to generate?", 100, 5000, 1500, step=100, key="n2")
    real = _seed_data(seed=3)
    st.caption("Treat this seed as sensitive, private records we may not share…")
    _validate_block(real, n)
    st.success(
        "The synthetic set reproduces the population's patterns while the privacy check shows no "
        "real record was copied — safe to share and model on.")
```

- [ ] **Step 4: Run test + manual check**

Run: `python3 -m pytest tests/test_page_synthetic.py -v`
Expected: PASS

Manual: `streamlit run Home.py` → open "Collect Synthetic" in the sidebar → both tabs render, the slider regenerates, the scatter overlays real vs synthetic, privacy metrics show 0% exact copies.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: add Synthetic Data demo page (augmentation + privacy tabs)"
```

---

### Task 6: Home page — the lifecycle map

**Files:**
- Modify: `Home.py`
- Test: `tests/test_home.py`

**Interfaces:**
- Produces: a Home page that shows the lifecycle and orients the audience.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_home.py
from streamlit.testing.v1 import AppTest

def test_home_loads_and_shows_lifecycle():
    at = AppTest.from_file("Home.py").run()
    assert not at.exception
    body = " ".join(m.value for m in at.markdown)
    assert "Collect" in body and "Decision" in body
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_home.py -v`
Expected: FAIL — "Collect"/"Decision" not found (current Home lacks the lifecycle map).

- [ ] **Step 3: Update Home**

```python
# Home.py
import streamlit as st

st.set_page_config(page_title="Data to Decisions", page_icon="📊", layout="wide")
st.title("📊 Data to Decisions")
st.subheader("An interactive tour of how data becomes a decision")
st.markdown(
    "Use the sidebar to move through the workshop. Each **📊 page** is a slide and each "
    "**🧪 page** is a live demo. The demos follow one small business — *Nour Store* — from "
    "raw, messy data all the way to a decision."
)
st.markdown("### The journey")
st.markdown(
    "**Collect** → **Clean** → **Filter** → **Analyze** → **Engineer** → **Predict** → **Decision**"
)
st.graphviz_chart("""
digraph { rankdir=LR; node [shape=box, style=rounded];
  Collect -> Clean -> Filter -> Analyze -> Engineer -> Predict -> Decision; }
""")
st.info("Pick a page from the sidebar to begin.")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_home.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: Home page with the data lifecycle map"
```

---

## Self-Review

**Spec coverage (Phase 1 scope):** app shell + sidebar (Task 1, 6), shared story data `store_data`
(Task 2), shared UI `ui` (Task 3), synthesizer + validation `synth` (Task 4), Synthetic demo with both
tabs + generate→validate + honesty note (Task 5). Collection/transform/slides demos are later phases
per spec §7 — intentionally out of this plan.

**Placeholder scan:** none — every step has runnable code or an exact command.

**Type consistency:** `messy_orders`/`clean_orders` signatures match across store_data and its tests;
`generate`/`utility_report`/`privacy_report` names and return keys (`corr_abs_diff`, `min_distance`,
`exact_match_frac`, per-column `real_mean`/`synth_mean`) match between synth.py, its tests, and the
page's `_validate_block`. `ui.page_header`/`leader_takeaway` consistent across ui.py and the page.
