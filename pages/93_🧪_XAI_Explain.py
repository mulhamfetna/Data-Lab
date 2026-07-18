import pandas as pd
import streamlit as st

from workshop import explain, ui, visuals

st.set_page_config(page_title="Explain a prediction", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Explain one prediction — in plain words",
    "A global chart tells you what the model uses in general. But when the model flags *this* "
    "customer, you need to explain *this* decision — to the customer, to a colleague, to a "
    "regulator. Here we start from a typical customer and turn on this one's real values, one "
    "at a time, to see exactly what tipped the scale.",
)

clf, X, y, meta = explain.trained()
cols = meta["columns"]

st.markdown("### Describe a customer")
c = st.columns(3)
n_orders = c[0].slider("Number of orders", 1, 30, 18)
total_qty = c[1].slider("Total items bought", 1, 100, 70)
avg_amount = c[2].slider("Average order amount ($)", 1.0, 60.0, 45.0)
feats = {"n_orders": n_orders, "total_qty": total_qty, "avg_amount": avg_amount}

rep = explain.explain_prediction(clf, feats, X, cols)

left, right = st.columns([1, 2])
with left:
    label = "High-value 💎" if rep["final_proba"] >= 0.5 else "Regular"
    st.markdown(visuals.person_svg(rep["final_proba"], label), unsafe_allow_html=True)
with right:
    st.metric("High-value probability", f"{rep['final_proba']*100:.0f}%",
              f"{(rep['final_proba']-rep['baseline_proba'])*100:+.0f} pts vs a typical customer")
    st.markdown("**Why this prediction:**")
    for line in explain.narrate(rep["contributions"]):
        st.markdown(f"- {line}")

st.markdown("### Every feature's push (from the typical-customer baseline)")
contrib = pd.DataFrame({"feature": [explain.friendly(k) for k in rep["contributions"]],
                        "push on score": list(rep["contributions"].values())})
contrib = contrib[contrib["push on score"] != 0]
st.bar_chart(contrib, x="feature", y="push on score")
st.caption("Bars above zero pushed toward *high-value*, below zero away from it. This is an "
           "occlusion approximation — it ignores some feature interactions, but it's honest "
           "about the direction and rough size of each effect.")

ui.leader_takeaway("‘The model said no’ is never good enough. A per-decision explanation like "
                   "this is what makes an AI decision defensible — and often what the law now "
                   "requires.")
ui.footer()
