import streamlit as st

from workshop import queries as q, store_data as sd, ui, visuals

st.set_page_config(page_title="Internal Data", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Client / Internal Data — the goldmine you already own",
    "Before you scrape or buy anything, look inward: your CRM, invoices, order history, "
    "support tickets, and logs. Most businesses are sitting on the richest dataset they'll "
    "ever have — and never use it.",
)

st.markdown("#### Where internal data hides")
st.graphviz_chart("""
digraph { rankdir=LR; bgcolor="transparent";
  node [shape=box, style="rounded,filled", fontname="sans", fillcolor="#eef3f8", color="#c9ccd1"];
  Business [shape=oval, fillcolor="#cfe6f5"];
  Business -> "CRM /\\ncontacts"; Business -> "Invoices /\\nsales"; Business -> "Support\\ntickets";
  Business -> "Website /\\napp logs"; Business -> "Inventory"; }
""")

df = sd.clean_orders(sd.messy_orders())
st.markdown("#### Example: Nour Store's own order records")
c = st.columns(3)
c[0].metric("Orders on file", f"{len(df):,}")
c[1].metric("Customers", f"{df['customer_name'].nunique():,}")
c[2].metric("Revenue recorded", f"${df['amount'].sum():,.0f}")
st.dataframe(df.head(15), use_container_width=True)

st.markdown("**Even a plain order table already answers real questions:**")
st.bar_chart(q.revenue_by(df, "city"), x="city", y="revenue", color=visuals.PALETTE[0])
ui.leader_takeaway("Audit what you already collect before spending a dinar acquiring more.")
