import streamlit as st

from workshop import queries as q, report, store_data as sd, ui, visuals

st.set_page_config(page_title="Report", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Report — the whole story on one page",
    "The lifecycle ends where it started: a decision-maker. A report isn't a data dump — "
    "it's the headline numbers, the evidence, and the one recommendation a leader acts on "
    "this week.",
)

df = sd.clean_orders(sd.messy_orders())
k = report.kpis(df)

st.markdown("## Nour Store — Performance Report")
c = st.columns(4)
c[0].metric("Orders", f"{k['orders']:,}")
c[1].metric("Revenue", f"${k['revenue']:,.0f}")
c[2].metric("Avg order", f"${k['avg_order']:,.2f}")
c[3].metric("Delivered", f"{k['delivered_pct']}%")

st.markdown("### 1 · What sells")
col1, col2 = st.columns(2)
with col1:
    st.bar_chart(q.revenue_by(df, "product"), x="product", y="revenue", color=visuals.PALETTE[0])
with col2:
    st.bar_chart(q.revenue_by(df, "city"), x="city", y="revenue", color=visuals.PALETTE[2])

st.markdown("### 2 · When it sells")
st.line_chart(q.monthly_revenue(df), x="month", y="revenue")

st.markdown("### 3 · Order health")
status = df["status"].value_counts().rename_axis("status").reset_index(name="orders")
st.bar_chart(status, x="status", y="orders", color=visuals.PALETTE[1])

st.markdown("### 4 · Recommendation")
st.success(f"**Stock and market *{k['top_product']}* in *{k['top_city']}* next month.** It is the "
           f"top product and strongest city, and {k['delivered_pct']}% of orders are already "
           "delivered — the growth lever is demand, not fulfilment.")

st.download_button("⬇️ Download the full report (txt)", report.summary_text(k),
                   file_name="nour_store_report.txt", mime="text/plain")

st.divider()
st.markdown("### This is exactly what the big players publish")
st.markdown(
    "Same shape, bigger stage — real, free reports and open data you can read tonight:\n\n"
    "- **World Bank Open Data** — global development indicators · https://data.worldbank.org\n"
    "- **Our World in Data** — research + charts on the world's biggest problems · https://ourworldindata.org\n"
    "- **UN Data** — the United Nations statistics portal · https://data.un.org\n"
    "- **OECD Data** — economic & social data across countries · https://data.oecd.org\n"
    "- **Eurostat** — the EU's official statistics · https://ec.europa.eu/eurostat\n"
    "- **data.gov** — the US government's open-data catalogue · https://data.gov\n"
    "- **McKinsey — The State of AI** — annual corporate AI-adoption report · "
    "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai\n"
    "- **WEF — Future of Jobs Report** · https://www.weforum.org/reports"
)
ui.leader_takeaway("Every one of these is your Nour Store report at national or global scale — "
                   "same lifecycle, same discipline.")
