import pandas as pd
import streamlit as st

from workshop import market_basket as mb, ui

st.set_page_config(page_title="Market Basket", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Market Basket — 'customers who buy X also buy Y'",
    "Hidden in every set of receipts are buying patterns you can act on: bundle them, place "
    "them together, recommend one when the other is in the cart. This is the analysis behind "
    "every 'frequently bought together'.",
)

min_support = st.slider("Minimum support (how common the pair must be)", 0.01, 0.20, 0.03, 0.01)
r = mb.rules(mb.transactions(seed=0), min_support=min_support)

if r:
    top = r[0]
    st.success(f"**Customers who buy {top['if']} also buy {top['then']} "
               f"{top['confidence']*100:.0f}% of the time** — {top['lift']}× more than chance.")
    st.dataframe(pd.DataFrame(r), use_container_width=True)
    st.caption("**support** = how often the pair appears · **confidence** = P(then | if) · "
               "**lift** > 1 means a real association, not coincidence.")
else:
    st.info("No rules above this support — lower the threshold.")
ui.leader_takeaway("Bundles, placement, and 'frequently bought together' all come from this one "
                   "table — free revenue hiding in receipts you already have.")
