import pandas as pd
import streamlit as st

from workshop import fairness as fr, ui

st.set_page_config(page_title="Fairness Audit", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Fairness Audit — does the model treat everyone equally?",
    "Models learn from history, and history has bias. A fairness audit checks whether outcomes "
    "differ by group — even among people who equally deserve them. Skipping it means quietly "
    "automating yesterday's discrimination at scale.",
)

df = fr.make_data(seed=0)
a = fr.audit(df)

st.markdown("#### Approval rate by city")
st.bar_chart(pd.DataFrame({"city": list(a["overall"]), "approval rate": list(a["overall"].values())}),
             x="city", y="approval rate")

st.markdown("#### The real test: among **equally qualified** customers (high spend)")
c1, c2 = st.columns(2)
for col, (city, rate) in zip([c1, c2], a["among_qualified"].items()):
    col.metric(f"{city} — approved when qualified", f"{rate*100:.0f}%")

st.error(f"⚠️ **Fairness gap of {a['gap']*100:.0f} points.** Two customers with the same spend get "
         "different answers depending on their city — the model inherited a historical bias.")
st.info("Fairness metrics (demographic parity, equal opportunity) catch this. The fix is in the "
        "data and the objective, not a disclaimer.")
ui.leader_takeaway("An unaudited model can automate discrimination faster than any human — check "
                   "group outcomes before you trust, deploy, or buy one.")
