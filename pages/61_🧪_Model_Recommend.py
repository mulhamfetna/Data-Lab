import pandas as pd
import streamlit as st

from workshop import market_basket as mb, recommend as rc, ui

st.set_page_config(page_title="Recommendations", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Recommendation Engine — 'you might also like…'",
    "Amazon's recommender is estimated to drive ~35% of its revenue — and the core idea is "
    "simple: learn what gets bought together, then suggest it. Every 'frequently bought "
    "together' and 'recommended for you' starts here.",
)

item = st.selectbox("A customer just added…", mb.ITEMS)
recs = rc.recommend(item, k=3)

if recs:
    st.markdown(f"#### Because they bought **{item}**, recommend:")
    for name, strength in recs:
        st.markdown(f"- **{name}**  ·  bought together {strength} times")
    st.dataframe(pd.DataFrame(recs, columns=["recommended", "co-purchases"]),
                 use_container_width=True)
else:
    st.info("No strong co-purchases learned for this item yet.")
ui.leader_takeaway("A recommender is one of the highest-ROI models a business can ship — it turns "
                   "existing purchase data directly into extra basket size.")
