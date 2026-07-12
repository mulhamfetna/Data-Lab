import streamlit as st

from workshop import queries as q, store_data as sd, ui

st.set_page_config(page_title="Analyze", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Analyze — turning rows into a decision",
    "Analysis answers the business question: what sells, where, and when. The goal isn't "
    "a pretty chart — it's the one sentence a leader acts on.",
)

df = sd.clean_orders(sd.messy_orders())
by_product = q.revenue_by(df, "product")
by_city = q.revenue_by(df, "city")
monthly = q.monthly_revenue(df)

top_product = by_product.iloc[0]
top_city = by_city.iloc[0]
st.success(f"**Headline:** *{top_product['product']}* is the top earner "
           f"(${top_product['revenue']:,.0f}); *{top_city['city']}* is the strongest city "
           f"(${top_city['revenue']:,.0f}). Stock and market accordingly.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Revenue by product**")
    st.bar_chart(by_product, x="product", y="revenue")
with col2:
    st.markdown("**Revenue by city**")
    st.bar_chart(by_city, x="city", y="revenue")

st.markdown("**Revenue over time**")
st.line_chart(monthly, x="month", y="revenue")
