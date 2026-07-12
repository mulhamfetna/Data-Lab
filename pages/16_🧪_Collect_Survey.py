import streamlit as st

from workshop import sources, ui

st.set_page_config(page_title="Survey Data", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Survey / Quantitative Data — from raw responses to a number",
    "Surveys, sensors, and transactions arrive as numbers — but raw numbers lie until "
    "they're cleaned. Watch a satisfaction survey travel from messy raw responses to a "
    "single figure a leader can act on.",
)

raw = sources.raw_survey()
clean = sources.clean_survey(raw)

t1, t2, t3, t4 = st.tabs(["1 · Raw survey", "2 · Pre-cleaning", "3 · Cleaned", "4 · Visualized"])

with t1:
    st.markdown("**Raw survey responses** — straight out of the form, warts and all.")
    st.dataframe(raw, use_container_width=True)
    c = st.columns(3)
    c[0].metric("Responses", len(raw))
    c[1].metric("Duplicate rows", int(raw.duplicated().sum()))
    c[2].metric("Missing / invalid", int(raw[["satisfaction", "recommend", "value_for_money"]]
                                        .isna().to_numpy().sum()))

with t2:
    st.markdown("**Pre-cleaning:** what has to be fixed before *any* average is trustworthy —")
    st.markdown("- drop duplicate submissions\n- null out-of-range answers (a `9` on a 1–5 scale)\n"
                "- drop incomplete responses")
    st.caption("Skip this and every number downstream is quietly wrong.")

with t3:
    st.markdown("**Cleaned:** every row is now a valid, complete response.")
    st.dataframe(clean, use_container_width=True)
    st.caption(f"{len(raw)} raw → {len(clean)} clean responses.")

with t4:
    st.markdown("**Visualized:** the numbers a leader acts on.")
    summ = sources.survey_summary(clean["satisfaction"].tolist())
    c = st.columns(3)
    c[0].metric("Valid responses", summ["n"])
    c[1].metric("Avg satisfaction", summ["mean"])
    c[2].metric("% satisfied (4–5)", f"{summ['top_box_pct']}%")
    st.bar_chart(summ["distribution"])
    ui.leader_takeaway("The headline isn't the raw pile of responses — it's ‘82% satisfied’, "
                       "and only after cleaning is that number true.")
