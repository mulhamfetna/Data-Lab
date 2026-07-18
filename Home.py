import streamlit as st

from workshop import ui
from workshop.i18n import t

st.set_page_config(page_title="Data to Decisions", page_icon="📊", layout="wide")
lang = ui.language_toggle()
rtl = 'dir="rtl" style="text-align:right"' if lang == "ar" else ""

st.title(f"📊 {t('title', lang)}")
st.markdown(f'<div {rtl}><h3>{t("subtitle", lang)}</h3>{t("intro", lang)}</div>',
            unsafe_allow_html=True)

st.markdown(f"### {t('journey', lang)}")
st.markdown(
    f"**{t('Collect', lang)}** → **{t('Clean', lang)}** → **{t('Analyze', lang)}** → "
    f"**{t('Decision', lang)}**")
st.graphviz_chart("""
digraph { rankdir=LR; node [shape=box, style=rounded];
  Collect -> Clean -> Filter -> Analyze -> Engineer -> Predict -> Decision; }
""")

st.markdown("### ✋ Before we start")
word = st.text_input("What's the first word that comes to mind when you hear **“data”**?")
if word:
    st.info(f"You walked in thinking *“{word}”* — let's see where that goes by the end.")

st.caption(t("begin", lang))
