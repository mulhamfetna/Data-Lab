import os

import streamlit as st

from workshop.i18n import t

# Keys the GenAI demos read from os.environ. On Streamlit Community Cloud these arrive via
# st.secrets, not the environment, so we bridge them across once per page load.
_SECRET_KEYS = ("GROQ_API_KEY", "OPENROUTER_API_KEY", "HF_TOKEN", "OLLAMA_HOST",
                "LLM_PROVIDER", "LLM_MODEL")


def load_secrets_to_env() -> None:
    """Copy any configured provider keys from st.secrets into os.environ (cloud deploys).

    A no-op locally (no secrets file) — wrapped so a missing secrets store never raises.
    """
    try:
        for key in _SECRET_KEYS:
            if key not in os.environ and key in st.secrets:
                os.environ[key] = str(st.secrets[key])
    except Exception:
        pass


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
    load_secrets_to_env()
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
