import streamlit as st

from workshop import clustering as cl, store_data as sd, ui

st.set_page_config(page_title="Segmentation", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Segmentation — the customer tribes you didn't know you had",
    "Not all customers are the same, but you can't treat each one individually. Clustering finds "
    "a handful of natural groups — big spenders, one-time buyers, regulars — so you can tailor "
    "pricing, offers, and attention to each.",
)

df = sd.clean_orders(sd.messy_orders())
feats = cl.customer_features(df)
k = st.slider("How many segments?", 2, 6, 3)
seg = cl.segment(feats, k=k, seed=0)

st.markdown("#### Segments by spend and order frequency")
seg_view = seg.copy()
seg_view["segment"] = "Segment " + seg_view["segment"].astype(str)
st.scatter_chart(seg_view, x="n_orders", y="total_spend", color="segment")

st.markdown("#### Segment profiles")
st.dataframe(cl.profiles(seg), use_container_width=True)
st.caption("Each segment is a group of customers who behave alike — read the profiles to name "
           "them ('high-spend regulars', 'one-time small baskets') and act accordingly.")
ui.leader_takeaway("Segmentation turns 'all customers' into 3–4 groups you can actually build "
                   "strategies for — the foundation of targeted marketing.")
