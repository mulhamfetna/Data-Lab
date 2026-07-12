import streamlit as st

from workshop import sources, store_data as sd, ui

st.set_page_config(page_title="Other Data Sources", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 The Other Data Sources — you already own more than you think",
    "Beyond scraping and APIs, three sources sit right under your nose: your own internal "
    "records, the interviews and feedback you already collect, and the surveys you already "
    "run. Most leaders are world-class at these and never called it 'data collection.'",
)

tab1, tab2, tab3 = st.tabs(["1 · Client / internal data", "2 · Qualitative", "3 · Quantitative"])

with tab1:
    st.markdown(
        "**Client / internal data** — your CRM, invoices, forms, order history. This is the "
        "richest source most businesses ignore. Here's Nour Store's own order records:"
    )
    st.dataframe(sd.clean_orders(sd.messy_orders()).head(20), use_container_width=True)
    st.caption("Every business is already sitting on a dataset like this.")

with tab2:
    st.markdown(
        "**Qualitative methods** — interviews, feedback, reviews. Words become data when you "
        "count the themes."
    )
    default = ("the delivery was slow\ngreat product but slow support\nfast and friendly service\n"
               "delivery took too long\nloved it, will buy again\nsupport was unhelpful and slow")
    text = st.text_area("Customer feedback (one per line)", value=default, height=140)
    feedback = [line for line in text.splitlines() if line.strip()]
    themes = {"speed / delivery": ["slow", "fast", "long", "delivery", "quick"],
              "support": ["support", "help", "unhelpful", "friendly", "service"],
              "loyalty": ["again", "loved", "love", "great"]}
    counts = sources.theme_counts(feedback, themes)
    st.bar_chart(counts)
    st.caption(f"{len(feedback)} comments → {len(themes)} themes you can act on.")

with tab3:
    st.markdown(
        "**Quantitative methods** — surveys, sensors, transactions. Numbers you can average, "
        "track, and target. Here's a 1–5 satisfaction survey:"
    )
    responses = [5, 4, 4, 3, 5, 2, 4, 5, 3, 4, 5, 1, 4, 4, 3]
    st.write("Responses:", responses)
    s = sources.survey_summary(responses)
    c = st.columns(3)
    c[0].metric("Responses", s["n"])
    c[1].metric("Average score", s["mean"])
    c[2].metric("% satisfied (4–5)", f"{s['top_box_pct']}%")
    st.bar_chart(s["distribution"])
