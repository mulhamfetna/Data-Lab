import numpy as np
import pandas as pd
import streamlit as st

from workshop import drift as d, ui

st.set_page_config(page_title="Data Drift", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Data Drift — your model quietly going stale",
    "A model is only right while the world matches its training data. When customers, prices, or "
    "behaviour shift, accuracy erodes silently. Drift monitoring is the smoke alarm that says "
    "'retrain me' before the numbers go wrong.",
)

shift = st.slider("How much has the live data moved since training?", 0.0, 25.0, 0.0, 1.0)
ref = d.reference()
cur = d.live(shift)
rep = d.report(ref, cur)

hist = pd.DataFrame({"value": np.concatenate([ref, cur]),
                     "period": ["training"] * len(ref) + ["live"] * len(cur)})
st.markdown("#### Training vs live distribution")
st.bar_chart(hist.pivot_table(index=pd.cut(hist["value"], 20, labels=False),
                              columns="period", values="value", aggfunc="count").fillna(0))

c1, c2 = st.columns(2)
c1.metric("Drift score (PSI)", rep["psi"])
c2.metric("Status", rep["verdict"])
if rep["drifted"]:
    st.error("🚨 **Significant drift** — the live data no longer matches training. Retrain before "
             "trusting predictions.")
elif rep["psi"] >= 0.1:
    st.warning("⚠️ Moderate drift — keep watching.")
else:
    st.success("✅ Stable — the model's world still looks like its training data.")
st.caption("Rule of thumb: PSI < 0.1 stable · 0.1–0.25 moderate · > 0.25 significant.")
ui.leader_takeaway("Models don't fail loudly — they drift. Monitoring is what turns a silent "
                   "decline into an actionable alert.")
