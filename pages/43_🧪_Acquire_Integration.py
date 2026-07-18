import streamlit as st

from workshop import integration as ig, ui

st.set_page_config(page_title="Data Integration", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Data Integration — when your systems don't agree",
    "Every business has data in 6 places that never quite match: the CRM says 'Ahmad', the "
    "invoices say ' ahmad '. Integration is 90% reconciling keys so the pieces line up — get "
    "it wrong and half your customers vanish from the report.",
)

left, right = ig.sources(seed=0)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Source A — customer list** (clean keys)")
    st.dataframe(left, use_container_width=True, height=240)
with c2:
    st.markdown("**Source B — loyalty system** (messy keys)")
    st.dataframe(right, use_container_width=True, height=240)

naive = ig.naive_merge(left, right)
fixed = ig.reconciled_merge(left, right)

st.markdown("#### Join on the raw key vs. reconcile first")
m1, m2 = st.columns(2)
m1.metric("Naïve merge — matched", f"{ig.match_rate(naive)*100:.0f}%",
          help="Joining on the raw name; mismatched keys silently drop out.")
m2.metric("After key reconciliation", f"{ig.match_rate(fixed)*100:.0f}%",
          help="Normalise whitespace + casing on both sides, then join.")

st.warning("The naïve join looks like it worked — but silently lost the customers whose names "
           "didn't match exactly. That missing loyalty data would quietly skew every report.")
st.dataframe(fixed, use_container_width=True)
ui.leader_takeaway("When two systems disagree, the fix is almost never a fancy tool — it's "
                   "agreeing on a clean key.")
