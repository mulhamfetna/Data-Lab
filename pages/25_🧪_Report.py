import streamlit as st

from workshop import queries as q, report, store_data as sd, ui

st.set_page_config(page_title="Report", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Report — the decision, on one page",
    "The lifecycle ends where it started: a decision-maker. A good report isn't a data dump "
    "— it's the handful of numbers and the one recommendation a leader acts on this week.",
)

df = sd.clean_orders(sd.messy_orders())
k = report.kpis(df)

st.markdown("### Nour Store — this period at a glance")
c = st.columns(4)
c[0].metric("Orders", f"{k['orders']:,}")
c[1].metric("Revenue", f"${k['revenue']:,.0f}")
c[2].metric("Avg order", f"${k['avg_order']:,.2f}")
c[3].metric("Delivered", f"{k['delivered_pct']}%")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Revenue by product**")
    st.bar_chart(q.revenue_by(df, "product"), x="product", y="revenue")
with col2:
    st.markdown("**Revenue over time**")
    st.line_chart(q.monthly_revenue(df), x="month", y="revenue")

st.success(f"**Recommendation:** *{k['top_product']}* is the top earner and *{k['top_city']}* "
           "the strongest market — concentrate stock and marketing there next month.")

st.download_button("⬇️ Download the report (txt)", report.summary_text(k),
                   file_name="nour_store_report.txt", mime="text/plain")
