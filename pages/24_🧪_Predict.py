import pandas as pd
import streamlit as st

from workshop import model, store_data as sd, ui

st.set_page_config(page_title="Predict", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Predict — train an AI in 90 seconds",
    "A model learns patterns from past customers to flag the high-value ones — so you know "
    "who to nurture before they even place their next order. It's a real model on our data; "
    "bigger teams use the same idea at far larger scale.",
)

df = sd.clean_orders(sd.messy_orders())
X, y = model.build_features(df)
clf, metrics = model.train(X, y, seed=0)

c = st.columns(2)
c[0].metric("Model accuracy", f"{metrics['accuracy']*100:.0f}%")
c[1].metric("Customers learned from", f"{len(X):,}")

st.markdown("**What the model pays attention to**")
imp = pd.DataFrame({"feature": list(metrics["importance"]),
                    "importance": list(metrics["importance"].values())})
st.bar_chart(imp.head(6), x="feature", y="importance")

st.markdown("### Try it — describe a customer")
col = st.columns(3)
n_orders = col[0].slider("Number of orders", 1, 30, 5)
total_qty = col[1].slider("Total items bought", 1, 100, 12)
avg_amount = col[2].slider("Average order amount ($)", 1.0, 60.0, 20.0)

feats = {"n_orders": n_orders, "total_qty": total_qty, "avg_amount": avg_amount}
out = model.predict_one(clf, feats, metrics["columns"])
if out["label"] == 1:
    st.success(f"💎 Likely a **high-value** customer (confidence {out['proba']*100:.0f}%)")
else:
    st.info(f"Likely a **regular** customer (high-value confidence {out['proba']*100:.0f}%)")
