import streamlit as st

from workshop import queries as q, store_data as sd, ui

st.set_page_config(page_title="Filter", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Filter — asking a question of your data",
    "Filtering isn't deleting — it's zooming in. 'Show me delivered orders in Aleppo "
    "last quarter' is how a leader turns a mountain of rows into the slice that answers "
    "their question.",
)

df = sd.clean_orders(sd.messy_orders())

col1, col2 = st.columns(2)
cities = col1.multiselect("Cities", sorted(df["city"].unique()))
statuses = col2.multiselect("Order status", sorted(df["status"].unique()))
dmin, dmax = df["order_date"].min(), df["order_date"].max()
date_from, date_to = st.slider("Order date range", min_value=dmin.to_pydatetime(),
                               max_value=dmax.to_pydatetime(),
                               value=(dmin.to_pydatetime(), dmax.to_pydatetime()))
min_amount = st.slider("Minimum order amount", 0.0, float(df["amount"].max()), 0.0)

out = q.filter_orders(df, cities=cities or None, statuses=statuses or None,
                      date_from=date_from, date_to=date_to, min_amount=min_amount)

c = st.columns(3)
c[0].metric("Orders matched", f"{len(out):,}", f"{len(out) - len(df):,}")
c[1].metric("Revenue in view", f"${out['amount'].sum():,.0f}")
c[2].metric("Share of all orders", f"{100*len(out)/len(df):.0f}%")
st.dataframe(out.head(50), use_container_width=True)
