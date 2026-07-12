import streamlit as st

st.set_page_config(page_title="Close", page_icon="📊", layout="wide")
st.title("📊 Close — three things to do tonight")

st.markdown("1. **See your data** — name the one dataset your work already sits on (Source #1–7).")
st.markdown("2. **See the market** — open LinkedIn → read 5 job descriptions for the role nearest "
            "your problem.")
st.markdown("3. **Take one rung** — pick ONE step from the roadmap and put a date on it.")

st.markdown(
    "> The goal was never to make you an engineer — it's to make sure that in the next data or AI "
    "decision your network faces, **you're the one asking the sharp question.**"
)

st.markdown("### ✋ What will you actually do first?")
choice = st.radio("Pick one", [
    "See my data", "Read 5 job descriptions", "Take one roadmap step", "Share this with my team",
], index=None)
if choice:
    st.success(f"**{choice}** — that's your first move. The full 8-phase roadmap PDF is yours to keep.")

st.caption("Thank you. Now — what's the one thing stopping you from starting?")
