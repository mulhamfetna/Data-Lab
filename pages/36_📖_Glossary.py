import streamlit as st

from workshop import glossary as gl, ui

st.set_page_config(page_title="Glossary", page_icon="📖", layout="wide")
ui.page_header(
    "📖 Glossary — the whole lab's vocabulary, EN + العربية",
    "Jargon is where non-programmers stall. Every term used in this lab, in plain language, in "
    "both English and Arabic — search it in either language whenever a word trips you up.",
)

q = st.text_input("🔎 Search a term (English or العربية)", "")
results = gl.search(q)
st.caption(f"{len(results)} of {len(gl.GLOSSARY)} terms")

for e in results:
    with st.container(border=True):
        c1, c2 = st.columns(2)
        c1.markdown(f"**{e['en']}**")
        c1.caption(e["def_en"])
        c2.markdown(f"<div dir='rtl' style='text-align:right'><b>{e['ar']}</b><br>"
                    f"<span style='color:gray'>{e['def_ar']}</span></div>",
                    unsafe_allow_html=True)

if not results:
    st.info("No match. Try a shorter word, or clear the search to see every term.")

ui.leader_takeaway("Give your team the words. A shared, bilingual vocabulary is the quiet "
                   "foundation of every good conversation about data.")
ui.footer()
