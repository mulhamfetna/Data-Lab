import streamlit as st

from workshop import geospatial as geo, store_data as sd, ui

st.set_page_config(page_title="Geospatial", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Geospatial — where your business actually is",
    "Every order has a place, and place is a decision. Mapped, the data answers questions a "
    "table can't: where to open a hub, where to run a promotion, where delivery is stretched. "
    "Here are Nour Store's orders across five Syrian cities.",
)

df = sd.clean_orders(sd.messy_orders())
vols = geo.city_volumes(df)

st.markdown("### Orders on the map")
st.map(vols, latitude="lat", longitude="lon", size="orders", color="#0072B2")

st.markdown("### The numbers behind the map")
st.dataframe(vols[["city", "orders", "revenue"]], hide_index=True, use_container_width=True)
st.bar_chart(vols, x="city", y="orders", color="#0072B2")

lead = vols.iloc[0]
st.success(f"**{lead['city']}** leads with **{lead['orders']} orders** "
           f"(${lead['revenue']:,.0f} revenue). That's where a new hub or a targeted campaign "
           "would reach the most existing customers.")

ui.leader_takeaway("Ask to see the map, not just the table. Geography turns rows of orders into "
                   "decisions about hubs, delivery, and where to spend marketing.")
ui.footer()
