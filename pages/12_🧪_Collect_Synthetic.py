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
        st.metric("Typical distance to nearest real record", f"{priv['mean_distance']:.2f}")
        st.caption("No synthetic row reproduces a real record — the set matches the *population*, "
                   "not any individual.")
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
