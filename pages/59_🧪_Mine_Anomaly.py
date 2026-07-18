import streamlit as st

from workshop import anomaly as an, store_data as sd, ui

st.set_page_config(page_title="Anomaly Detection", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Anomaly Detection — the order that doesn't fit",
    "Fraud, errors, and surprises all look the same: a data point that breaks the pattern. "
    "Anomaly detection flags them automatically — a 400-unit order, a payment from nowhere — so "
    "a human can look before money moves.",
)

df = an.with_anomalies(sd.clean_orders(sd.messy_orders()), n=8, seed=0)
contamination = st.slider("How sensitive? (expected anomaly rate)", 0.01, 0.10, 0.03, 0.01)
df["anomaly"] = an.detect(df, contamination=contamination, seed=0)

flagged = int(df["anomaly"].sum())
st.metric("Orders flagged for review", flagged)

view = df.copy()
view["kind"] = view["anomaly"].map({True: "⚠️ anomaly", False: "normal"})
st.scatter_chart(view, x="quantity", y="amount", color="kind")
st.caption("Anomalies sit far from the crowd on quantity × amount — the model learns 'normal' "
           "and flags whatever doesn't fit.")

st.markdown("#### Flagged orders")
st.dataframe(df[df["anomaly"]][["order_id", "city", "product", "quantity", "amount"]],
             use_container_width=True)
ui.leader_takeaway("Automated anomaly flags are the difference between catching a fraudulent "
                   "order in seconds and finding it in next month's audit.")
