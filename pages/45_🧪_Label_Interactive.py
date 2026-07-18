import streamlit as st

from workshop import labeling, ui

st.set_page_config(page_title="Data Labeling", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Data Labeling — the human step behind every AI",
    "Before a model can learn, a human has to show it examples: this review is happy, that "
    "one isn't. Labeling is slow, expensive, and the quiet reason good AI is hard — the model "
    "is only ever as good as the labels you feed it.",
)

st.markdown("**Label a few reviews below, then train** — watch how just a handful of examples "
            "teaches the model to read the rest.")

reviews = [t for t, _ in labeling.POOL[:6]] + [t for t, _ in labeling.POOL[10:16]]
labeled = []
for i, text in enumerate(reviews):
    c1, c2 = st.columns([3, 2])
    c1.write(f"“{text}”")
    choice = c2.radio("label", ["—", "👍 positive", "👎 negative"], key=f"lab{i}",
                      horizontal=True, label_visibility="collapsed")
    if choice != "—":
        labeled.append((text, 1 if "positive" in choice else 0))

st.caption(f"You've labeled {len(labeled)} of {len(reviews)} reviews.")

if st.button("🎓 Train on my labels", type="primary"):
    out = labeling.train_and_eval(labeled)
    if out is None:
        st.warning("Label at least one 👍 **and** one 👎 — a model needs both to learn.")
    else:
        st.metric("Accuracy reading the rest of the reviews", f"{out['accuracy']*100:.0f}%",
                  help="Tested against the true sentiment of all 20 pool reviews.")
        st.success(f"From just {out['n_labeled']} labeled examples, the model now reads reviews it "
                   "has never seen. Label more and it gets sharper.")
        ui.leader_takeaway("‘We need more data’ usually means ‘we need more *labeled* data’ — and "
                           "that human labeling cost is the hidden budget line in every AI project.")
