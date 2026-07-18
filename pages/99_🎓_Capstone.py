import streamlit as st

from workshop import capstone as cap, ui

st.set_page_config(page_title="Capstone", page_icon="🎓", layout="wide")
ui.page_header(
    "🎓 Capstone — lead one data initiative, end to end",
    "This ties the whole session together. You're leading Nour Store's data initiative; at each "
    "stage of the lifecycle you make the call a leader actually makes. There are no coding "
    "questions — only judgement. Your score is how many good decisions you made.",
)

st.caption("Pick an answer at each stage, then score yourself at the bottom.")

answers = {}
for i, step in enumerate(cap.STEPS):
    st.markdown(f"#### {i+1}. {step['stage']}")
    choice = st.radio(step["question"], step["options"], key=f"cap_{i}", index=None)
    if choice is not None:
        answers[i] = step["options"].index(choice)

if st.button("🎓 Score my decisions"):
    if len(answers) < len(cap.STEPS):
        st.warning("Answer every stage first.")
    else:
        result = cap.grade(answers)
        st.metric("Score", f"{result['score']} / {result['max']}")
        st.progress(result["score"] / result["max"])
        st.success(cap.verdict(result["score"], result["max"]))
        for i, r in enumerate(result["results"]):
            icon = "✅" if r["correct"] else "❌"
            with st.expander(f"{icon} {i+1}. {r['stage']}"):
                st.markdown(f"**Best answer:** {cap.STEPS[i]['options'][r['best']]}")
                st.caption(r["why"])

ui.leader_takeaway("Leading with data isn't about writing code — it's a chain of good judgement "
                   "calls, one per stage. That chain is exactly what this whole lab has been "
                   "training.")
ui.footer()
