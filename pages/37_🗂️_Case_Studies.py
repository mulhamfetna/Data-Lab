import streamlit as st

from workshop import cases, ui

st.set_page_config(page_title="Case studies", page_icon="🗂️", layout="wide")
ui.page_header(
    "🗂️ Case studies — the lessons, with real names attached",
    "Every concept in this lab has already played out in the real world — some as billion-dollar "
    "wins, some as public disasters. Here are the stories behind the terms, each with the lesson "
    "and a source you can read.",
)

st.caption("Browse the cards; each links to a reputable source.")

cards = cases.cases()
cols = st.columns(2)
for i, c in enumerate(cards):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"### {c['icon']} {c['company']}")
            st.markdown(f"**{c['title']}**")
            st.write(c["what"])
            st.info(f"📎 **Lesson:** {c['lesson']}")
            st.caption(f"Maps to: *{c['epic']}*")
            st.markdown(f"[Read the source →]({c['link']})")

ui.leader_takeaway("For every technique, ask: *who has already done this — and what happened?* "
                   "These stories are the fastest way to learn where the value and the landmines "
                   "really are.")
ui.footer()
