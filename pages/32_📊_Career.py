import streamlit as st

st.set_page_config(page_title="Career Growth", page_icon="📊", layout="wide")
st.title("📊 Career Growth — proof beats certificates")

c1, c2 = st.columns(2)
c1.success("**Door A — Build proof**\n\nKaggle · datathons · portfolio projects · "
           "build-in-public on GitHub + LinkedIn.")
c2.info("**Door B — Find & grow talent**\n\nRead a portfolio, spot real skill vs. "
        "certificate-collectors, mentor, and hire.")

st.markdown("**One clean, deployed project beats ten finished courses.** For seniors, that same "
            "truth is your hiring filter — stop counting certificates, start reviewing *shipped work*.")

st.markdown("> 📎 **Story — Amazon's recommendation engine** drives an estimated **~35% of "
            "revenue** — and started simple, growing weekly. You don't start big; you ship small.")

st.markdown("### ✋ Rate this portfolio — who would you interview?")
candidates = {
    "A — 12 certificates, no projects": False,
    "B — one strong, deployed project": True,
    "C — ten half-finished tutorials": False,
}
pick = st.radio("Pick one", list(candidates), index=None)
if pick:
    if candidates[pick]:
        st.success("✅ The single **deployed** project wins — demonstrable skill beats volume.")
    else:
        st.warning("That's the trap. The candidate with **one shipped project** almost always "
                   "wins — the market pays for what you can *demonstrate*.")
