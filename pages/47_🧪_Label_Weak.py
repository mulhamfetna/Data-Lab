import pandas as pd
import streamlit as st

from workshop import labeling, weak, ui

st.set_page_config(page_title="Weak Supervision", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Weak Supervision — labeling by rules, not by hand",
    "Hand-labeling millions of rows is impossible. Instead you write a few cheap rules — "
    "'if it says slow, it's negative' — let them vote, and label a whole dataset in minutes. "
    "Noisier than a human, but it scales to where humans can't.",
)

st.markdown("#### The labeling functions (rules)")
c1, c2 = st.columns(2)
c1.info("**LF 1 — positive words** → votes 👍\n\n" + ", ".join(weak.POS[:8]) + " …")
c2.warning("**LF 2 — negative words** → votes 👎\n\n" + ", ".join(weak.NEG[:8]) + " …")

texts = [t for t, _ in labeling.POOL]
votes = weak.apply_lfs(texts)
preds = [weak.majority_vote(v) for v in votes]
table = pd.DataFrame({
    "review": texts,
    "LF positive": [v[0] for v in votes],
    "LF negative": [v[1] for v in votes],
    "auto label": ["👍" if p == 1 else "👎" if p == 0 else "— (abstain)" for p in preds],
})
st.dataframe(table, use_container_width=True, height=320)

r = weak.evaluate()
m1, m2 = st.columns(2)
m1.metric("Coverage (rows the rules labeled)", f"{r['coverage']*100:.0f}%")
m2.metric("Accuracy vs true labels", f"{r['accuracy']*100:.0f}%")
st.success(f"Two simple rules labeled {r['n_covered']} of {len(texts)} reviews at "
           f"{r['accuracy']*100:.0f}% accuracy — no human labeled a single one.")
ui.leader_takeaway("Weak supervision trades a little accuracy for enormous scale — it's how teams "
                   "bootstrap labels when hand-labeling is off the table.")
