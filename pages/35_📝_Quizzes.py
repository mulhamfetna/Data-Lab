import streamlit as st

from workshop import quiz, ui

st.set_page_config(page_title="Quizzes", page_icon="📝", layout="wide")
ui.page_header(
    "📝 Quizzes — make it stick",
    "A demo you watch fades; a question you answer sticks. Pick an epic and take a quick check — "
    "no code, just the judgement each stage was teaching. Instant feedback, with the reason for "
    "every right answer.",
)

epic = st.selectbox("Choose an epic to review", quiz.epics())
questions = quiz.QUIZZES[epic]

answers = {}
for i, item in enumerate(questions):
    st.markdown(f"#### {i+1}. {item['q']}")
    choice = st.radio("Pick one", item["options"], key=f"quiz_{epic}_{i}", index=None,
                      label_visibility="collapsed")
    if choice is not None:
        answers[i] = item["options"].index(choice)

if st.button("Check my answers"):
    if len(answers) < len(questions):
        st.warning("Answer every question first.")
    else:
        result = quiz.grade_quiz(epic, answers)
        st.metric("Score", f"{result['score']} / {result['max']}")
        st.progress(result["score"] / result["max"])
        for i, r in enumerate(result["results"]):
            if r["correct"]:
                st.success(f"{i+1}. Correct — {r['why']}")
            else:
                st.error(f"{i+1}. Not quite. Best answer: "
                         f"*{questions[i]['options'][r['best']]}* — {r['why']}")

ui.leader_takeaway("Recall beats recognition: answering a question locks in a lesson far better "
                   "than watching a demo. Use these as end-of-segment recaps.")
ui.footer()
