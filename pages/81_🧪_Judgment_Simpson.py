import streamlit as st

from workshop import simpson as sp, ui, visuals

st.set_page_config(page_title="Simpson's Paradox", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Simpson's Paradox — the winner that loses everywhere",
    "The single most dangerous trap in data: a headline number that reverses the moment you look "
    "closer. A campaign can 'win' overall while losing with every single customer group — trust "
    "the aggregate blindly and you'll back the wrong horse.",
)

st.markdown("#### The headline: which campaign converted better overall?")
ov = sp.overall_rates()
st.bar_chart(ov, x="campaign", y="rate", color=visuals.PALETTE[0])
winner = ov.loc[ov["rate"].idxmax(), "campaign"]
st.success(f"Overall, **Campaign {winner} wins** ({ov['rate'].max()}% vs {ov['rate'].min()}%). "
           "Case closed?")

st.markdown("#### Now split by customer segment…")
seg = sp.segment_rates()
st.dataframe(seg.pivot(index="segment", columns="campaign", values="rate"),
             use_container_width=True)
st.error("😳 **Campaign A wins in *every* segment** — new customers *and* returning — yet loses "
         "overall. The aggregate lied because the segments had very different sizes.")
st.info("Whenever you see one number comparing two groups, ask: **does it hold within every "
        "subgroup?** If a vendor won't show you the breakdown, be suspicious.")
ui.leader_takeaway("An average can point the exact opposite way from the truth — always demand "
                   "the segment breakdown before you decide.")
