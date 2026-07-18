import streamlit as st

from workshop import ui

st.set_page_config(page_title="Data Architectures", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 ETL vs ELT · Warehouse vs Lake — where your data lives",
    "You don't need to build these, but you fund and choose between them. Knowing the four words "
    "means you can tell whether a vendor's pitch fits your problem — or is selling you a lake you "
    "don't need.",
)

st.markdown("### ETL vs ELT — *when* do you clean the data?")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**ETL** — clean *before* loading (classic, structured)")
    st.graphviz_chart("""digraph { rankdir=LR; bgcolor="transparent"; node[shape=box,style="rounded,filled",fontname=sans,fillcolor="#eef3f8",color="#c9ccd1"];
      Extract -> Transform -> Load; Load[fillcolor="#d4efe4"]; }""")
with c2:
    st.markdown("**ELT** — load raw, clean *later* in the warehouse (modern, flexible)")
    st.graphviz_chart("""digraph { rankdir=LR; bgcolor="transparent"; node[shape=box,style="rounded,filled",fontname=sans,fillcolor="#eef3f8",color="#c9ccd1"];
      Extract -> Load -> Transform; Load[fillcolor="#d4efe4"]; }""")
st.caption("ELT won as storage got cheap: dump everything, transform on demand — more flexible, "
           "but you must govern the mess.")

st.divider()
st.markdown("### Warehouse vs Lake vs Lakehouse — *how* is it stored?")
st.markdown(
    "| | Data Warehouse | Data Lake | Lakehouse |\n"
    "|---|---|---|---|\n"
    "| **Holds** | clean, structured tables | raw everything (files, images, logs) | both |\n"
    "| **Best for** | dashboards & reporting | data science & ML | one system for all of it |\n"
    "| **Risk** | rigid, expensive | becomes a 'data swamp' | newer, still maturing |\n"
    "| **Examples** | Snowflake, BigQuery | S3 + files | Databricks, Delta Lake |"
)
st.graphviz_chart("""digraph { rankdir=LR; bgcolor="transparent"; node[shape=box,style="rounded,filled",fontname=sans,color="#c9ccd1"];
  Sources[shape=oval,fillcolor="#cfe6f5"];
  Sources -> Lake[label="raw"]; Lake -> Warehouse[label="cleaned"]; Warehouse -> BI[label="report"];
  Lake[fillcolor="#fbe6c2"]; Warehouse[fillcolor="#d4efe4"]; BI[label="Dashboards\\n& ML",fillcolor="#c9f0d8"]; }""")
ui.leader_takeaway("Warehouse = tidy answers, Lake = raw everything, Lakehouse = both. Match the "
                   "choice to whether your team mostly reports or mostly experiments.")
