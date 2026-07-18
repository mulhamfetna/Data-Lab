import streamlit as st

from workshop import pii, ui

st.set_page_config(page_title="PII Masking", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 PII Masking — hide the person, keep the pattern",
    "You can analyse customer behaviour without exposing who they are. Masking and pseudonymising "
    "personal data lets teams work, share, and comply with privacy law — while the analytics "
    "(spend, city, trends) stay fully intact.",
)

df = pii.sample(seed=0)
st.markdown("#### Raw records — full of personal data (PII)")
st.dataframe(df, use_container_width=True)

st.markdown("#### Anonymised — safe to share and analyse")
st.dataframe(pii.anonymize(df), use_container_width=True)

st.success("Names → initials, emails and phones → masked, a stable **hashed id** replaces the "
           "email (same person = same id, but not reversible). Spend and city are untouched, so "
           "every report still works.")
st.info("This is the everyday version of the same idea as the **Synthetic Data** demo: use the "
        "data's value without exposing individuals — the core of GDPR-style compliance.")
ui.leader_takeaway("Most analytics never needs to know *who* — masking PII removes legal risk at "
                   "almost no analytical cost.")
