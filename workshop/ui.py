import streamlit as st

from workshop.i18n import t


def current_lang() -> str:
    return st.session_state.get("lang", "en")


def language_toggle() -> str:
    """Sidebar English/Arabic switch; stored in session so it persists across pages."""
    choice = st.sidebar.radio(
        f"🌐 {t('language', current_lang())}", ["English", "العربية"],
        index=0 if current_lang() == "en" else 1, horizontal=True)
    st.session_state.lang = "ar" if choice == "العربية" else "en"
    return st.session_state.lang


def page_header(title: str, takeaway: str) -> None:
    st.title(title)
    leader_takeaway(takeaway)


def leader_takeaway(text: str) -> None:
    st.info(f"📎 **{t('takeaway', current_lang())}:** {text}")


def footer() -> None:
    st.markdown("---")
    st.caption(
        "**Neurobotics Academy** · Eng. Mulham Fetna · "
        "[Telegram](https://t.me/Mulham_Fetna_official) · "
        "[GitHub](https://github.com/mulhamfetna) · "
        "[YouTube](https://www.youtube.com/@eng.mulham-fetna) · "
        "[Instagram](https://instagram.com/mulham.robotics)")
