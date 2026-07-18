import pandas as pd
import streamlit as st

from workshop import optimize as opt, ui

st.set_page_config(page_title="Price optimization", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Optimization — the price that makes the most money",
    "More sales is not the goal — more profit is. Price too high and you sell too few; too low "
    "and you leave money on every unit. Optimization finds the peak. The same idea (an objective "
    "with a trade-off) is how the big platforms price, stock, and staff — here it's one clear "
    "curve you can point at.",
)

st.markdown("### Your product")
c = st.columns(3)
cost = c[0].slider("Unit cost ($)", 1.0, 15.0, 5.0, 0.5)
base = c[1].slider("Max demand (units at price 0)", 400, 1500, 1000, 50)
slope = c[2].slider("Price sensitivity", 20, 80, 40, 5)

curve = opt.profit_curve(cost=cost, base=base, slope=slope)
df = pd.DataFrame(curve, columns=["price", "profit"])
best = opt.optimal_price(cost=cost, base=base, slope=slope)

st.line_chart(df, x="price", y="profit")

c1, c2, c3 = st.columns(3)
c1.metric("Best price", f"${best['price']:.2f}")
c2.metric("Profit at that price", f"${best['profit']:,.0f}")
c3.metric("Units sold there", f"{best['units']:,}")

your_price = st.slider("Try a price yourself", 5.0, 25.0, 12.0, 0.5)
your_profit = opt.profit(your_price, cost, base, slope)
gap = best["profit"] - your_profit
if gap > 0:
    st.warning(f"At ${your_price:.2f} you'd make **${your_profit:,.0f}** — that's "
               f"**${gap:,.0f} less** than the optimum. Notice the peak isn't the highest price "
               "or the most units; it's the balance.")
else:
    st.success(f"That's essentially the optimal price — **${your_profit:,.0f}** profit.")

ui.leader_takeaway("‘Sell more’ and ‘charge more’ are both traps on their own. The money is at "
                   "the peak of the curve — and finding that peak is what optimization does, "
                   "for pricing and far beyond.")
ui.footer()
