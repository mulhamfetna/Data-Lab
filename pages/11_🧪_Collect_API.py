import streamlit as st

from workshop import live_api, ui

st.set_page_config(page_title="REST API", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 REST API — live data, from anywhere, instantly",
    "An API is a doorway another system opens for you. One request pulls fresh numbers — "
    "prices, weather, exchange rates — straight into your own tools, live, without anyone "
    "emailing you a spreadsheet.",
)

base = st.selectbox("Base currency", ["USD", "EUR", "GBP", "TRY"])
data = live_api.get_rates(base)

badge = "🟢 live" if data["source"] == "live" else "🟡 cached (offline)"
st.caption(f"{badge} · rates as of {data['date']}")

favourites = ["EUR", "GBP", "TRY", "JPY", "SAR", "AED"]
cols = st.columns(len(favourites))
for col, cur in zip(cols, favourites):
    rate = data["rates"].get(cur)
    if rate:
        col.metric(f"1 {base} →", f"{rate:.3f} {cur}")

st.markdown("### Convert an amount")
c1, c2 = st.columns(2)
amount = c1.number_input(f"Amount in {base}", min_value=0.0, value=100.0, step=10.0)
target = c2.selectbox("To", [c for c in data["rates"]], index=0)
converted = amount * data["rates"][target]
st.success(f"**{amount:,.2f} {base} = {converted:,.2f} {target}**")
