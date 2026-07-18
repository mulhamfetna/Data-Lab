import pandas as pd
import streamlit as st

from workshop import explain, ui

st.set_page_config(page_title="Feature attribution", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Feature attribution — what is the model actually using?",
    "Before you trust a model's decisions, you need to know what drives them. Attribution "
    "shuffles each input and measures how much the model's accuracy falls — a big fall means "
    "the model truly relies on that input. It's how you catch a model leaning on the wrong "
    "thing (a proxy for gender, a leaked ID) before it embarrasses you.",
)

clf, X, y, meta = explain.trained()
scores = explain.permutation_scores(clf, X, y)

st.caption("Same Predict model as the Predict demo — here we ask *why* it works.")
imp = pd.DataFrame({"feature": list(scores), "importance (accuracy drop when shuffled)":
                    list(scores.values())})
st.bar_chart(imp.head(8), x="feature", y="importance (accuracy drop when shuffled)")

top = imp.iloc[0]
st.success(f"The model leans most on **{top['feature']}** — shuffling it costs the most "
           "accuracy. Features near zero barely matter and could be dropped.")

with st.expander("Impurity importance vs permutation importance — why we use permutation"):
    st.markdown(
        "- **Impurity importance** (the quick number most libraries print) can inflate features "
        "with many distinct values, even random ones.\n"
        "- **Permutation importance** measures real predictive value — does accuracy actually "
        "drop when this feature is scrambled? That's the honest question.\n\n"
        "*Both are global averages and ignore some feature interactions — see the "
        "single-prediction demo for the per-customer view.*")

ui.leader_takeaway("Ask for a feature-attribution chart of any model before you deploy it. If it "
                   "relies on something it shouldn't, this is where you'll see it.")
ui.footer()
