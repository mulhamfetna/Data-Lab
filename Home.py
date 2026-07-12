import streamlit as st

st.set_page_config(page_title="Data to Decisions", page_icon="📊", layout="wide")
st.title("📊 Data to Decisions")
st.subheader("An interactive tour of how data becomes a decision")
st.markdown(
    "Use the sidebar to move through the workshop. Each **📊 page** is a slide and each "
    "**🧪 page** is a live demo. The demos follow one small business — *Nour Store* — from "
    "raw, messy data all the way to a decision."
)
st.markdown("### The journey")
st.markdown(
    "**Collect** → **Clean** → **Filter** → **Analyze** → **Engineer** → **Predict** → **Decision**"
)
st.graphviz_chart("""
digraph { rankdir=LR; node [shape=box, style=rounded];
  Collect -> Clean -> Filter -> Analyze -> Engineer -> Predict -> Decision; }
""")

st.markdown("### ✋ Before we start")
word = st.text_input("What's the first word that comes to mind when you hear **“data”**?")
if word:
    st.info(f"You walked in thinking *“{word}”* — let's see where that goes by the end.")

st.caption("Pick a page from the sidebar to begin.")
