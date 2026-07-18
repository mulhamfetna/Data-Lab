import pandas as pd
import streamlit as st

from workshop import dedup, ui

st.set_page_config(page_title="Deduplication", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Deduplication — is this the same person twice?",
    "The same customer sneaks into your database as 'Ahmad Ali', 'ahmad ali', and 'Ahmad  Ali'. "
    "Entity resolution finds these near-duplicates so you don't count one customer as three — "
    "or mail them three times.",
)

st.markdown("**The messy name list:**")
st.write(dedup.SAMPLE)

threshold = st.slider("Match sensitivity (higher = stricter)", 0.5, 1.0, 0.85, 0.05)
pairs = dedup.duplicate_pairs(dedup.SAMPLE, threshold)

st.markdown(f"#### {len(pairs)} likely-duplicate pairs at ≥ {threshold:.2f} similarity")
if pairs:
    st.dataframe(pd.DataFrame(pairs, columns=["name A", "name B", "similarity"]),
                 use_container_width=True)
else:
    st.info("No pairs above this threshold — try lowering the sensitivity.")
st.caption("Slide the threshold: too loose merges different people; too strict misses real "
           "duplicates. The sweet spot is a judgement call.")
ui.leader_takeaway("Duplicate customers quietly inflate your counts and waste your marketing — "
                   "entity resolution is unglamorous money-saving.")
