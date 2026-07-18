import streamlit as st

from workshop import ab, ui

st.set_page_config(page_title="A/B Testing", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 A/B Testing — proving a change actually worked",
    "You changed the button colour and sales rose 3%. Real effect, or luck? A/B testing splits "
    "traffic, measures both, and tells you whether the difference is signal or noise — the "
    "guardrail against fooling yourself.",
)

c = st.columns(3)
n = c[0].slider("Visitors per variant", 200, 5000, 1000, 100)
pa = c[1].slider("True rate — A (current)", 0.05, 0.30, 0.10, 0.01)
pb = c[2].slider("True rate — B (new)", 0.05, 0.30, 0.12, 0.01)

ca, cb = ab.simulate(n, pa, pb, seed=0)
r = ab.analyze(n, ca, n, cb)

m = st.columns(2)
m[0].metric("A — observed conversion", f"{r['rate_a']*100:.1f}%", f"{ca} of {n}")
m[1].metric("B — observed conversion", f"{r['rate_b']*100:.1f}%", f"{cb} of {n}")

if r["significant"]:
    st.success(f"✅ **Significant** (p = {r['pvalue']}). B beats A by {r['lift']}% — ship it.")
else:
    st.warning(f"⚠️ **Not significant** (p = {r['pvalue']}). The difference could be noise — "
               "keep testing or collect more data before deciding.")
st.caption("p-value < 0.05 = the result is unlikely to be chance. Small samples make even real "
           "effects look uncertain — which is why sample size matters.")
ui.leader_takeaway("A/B testing is the discipline that stops teams shipping changes that *felt* "
                   "like wins but weren't.")
