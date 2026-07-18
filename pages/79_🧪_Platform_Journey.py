import streamlit as st

from workshop import ui

st.set_page_config(page_title="My Journey", page_icon="🗺️", layout="wide")
ui.page_header(
    "🗺️ My Journey — track where you are in the data lifecycle",
    "Nine stages take raw data to a decision. Tick each as you explore it and watch your progress "
    "across the whole lifecycle — so nobody leaves having seen only half the story.",
)

STAGES = ["Collect", "Label", "Clean", "Encode", "Mine", "Analyze/Model",
          "Scale", "Govern", "Serve"]

if "journey" not in st.session_state:
    st.session_state.journey = set()

st.markdown("#### The nine stages")
cols = st.columns(3)
for i, stage in enumerate(STAGES):
    with cols[i % 3]:
        done = st.checkbox(stage, value=stage in st.session_state.journey, key=f"j_{stage}")
        if done:
            st.session_state.journey.add(stage)
        else:
            st.session_state.journey.discard(stage)

done_n = len(st.session_state.journey)
st.progress(done_n / len(STAGES), text=f"{done_n} / {len(STAGES)} stages explored")
if done_n == len(STAGES):
    st.success("🎉 You've walked the entire data lifecycle — from raw data to a governed, served "
               "decision.")
elif done_n >= len(STAGES) // 2:
    st.info("Halfway there — keep going through the sidebar demos.")
ui.leader_takeaway("Data literacy isn't one skill — it's the whole chain. Seeing every link is "
                   "what turns 'I've heard of AI' into 'I can judge it'.")
