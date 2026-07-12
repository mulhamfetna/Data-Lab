import streamlit as st

st.set_page_config(page_title="Why Data", page_icon="📊", layout="wide")
st.title("📊 Why Data — the vital role behind every decision")

st.markdown(
    "Every serious decision — pricing a product, approving a loan, planning a city, "
    "hiring a team — is really a bet on the future. **Data is how you stop guessing and "
    "start knowing.**"
)

st.markdown("### Decisions made with vs. without data")
c1, c2 = st.columns(2)
c1.error("**Gut only**\n\nFast, but blind to what you can't see. Confidently wrong.")
c2.success("**Gut + data**\n\nSame instincts, now checked against reality before you commit.")

st.graphviz_chart("""
digraph { rankdir=LR; bgcolor="transparent"; node [shape=box, style="rounded,filled",
  fontname="sans", color="#c9ccd1"];
  Q [label="A decision", shape=oval, fillcolor="#cfe6f5"];
  Q -> Gut [label="gut only"]; Q -> Data [label="gut + data"];
  Gut [label="Guess", fillcolor="#f6d5cf"]; Data [label="Check reality", fillcolor="#d4efe4"];
  Gut -> Wrong; Data -> Right;
  Wrong [label="Confidently wrong", fillcolor="#f6d5cf"];
  Right [label="Evidence-backed", fillcolor="#c9f0d8"]; }
""")

st.markdown(
    "> 📎 **Story — Target knew before the father did.** By analysing shopping patterns, "
    "Target's models flagged a teenager as pregnant — and mailed baby coupons — before her "
    "family knew. Data doesn't just describe the present; it predicts behaviour."
)

st.markdown("### ✋ Quick poll")
st.write("Name one major decision — personal, business, or national — made with **zero** data.")
choice = st.radio("Was that decision…", ["A great call", "A lucky escape", "A costly mistake"],
                  horizontal=True, index=None)
if choice:
    st.info(f"You picked **{choice}** — now imagine making that same call *with* the numbers in "
            "front of you. That gap is the whole workshop.")

st.divider()
st.caption("Next: how raw data actually becomes a decision → **The Lifecycle**.")
