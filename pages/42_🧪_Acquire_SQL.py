import streamlit as st

from workshop import sqlquery, store_data as sd, ui

st.set_page_config(page_title="SQL Extraction", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Database Extraction — asking your data questions in SQL",
    "Most business data lives in databases, and SQL is the universal language for pulling "
    "exactly what you need out of them. You don't have to write it — but recognising a clean "
    "query is how you know your analyst is asking the right thing.",
)

df = sd.clean_orders(sd.messy_orders())
st.caption(f"Connected to an in-memory database with {len(df):,} Nour Store orders "
           "(table: `orders`).")

preset = st.selectbox("Start from a question", list(sqlquery.PRESETS))
sql = st.text_area("SQL (SELECT only)", value=sqlquery.PRESETS[preset], height=140)

if st.button("▶️ Run query", type="primary"):
    try:
        result = sqlquery.run(sql, df)
        st.success(f"{len(result):,} rows")
        st.dataframe(result, use_container_width=True)
    except Exception as exc:
        st.error(f"Query error: {exc}")

ui.leader_takeaway("SQL turns 'which cities buy the most olive oil?' into an answer in one line — "
                   "it's the single most valuable technical skill for a non-engineer to recognise.")
