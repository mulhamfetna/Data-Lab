import streamlit as st


def page_header(title: str, takeaway: str) -> None:
    st.title(title)
    leader_takeaway(takeaway)


def leader_takeaway(text: str) -> None:
    st.info(f"📎 **Leader takeaway:** {text}")
