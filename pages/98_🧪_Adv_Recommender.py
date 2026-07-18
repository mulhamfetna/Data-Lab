import streamlit as st

from workshop import matrixfactor as mf, ui

st.set_page_config(page_title="Matrix-factorization recommender", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Matrix factorization — the 'you might also like' engine",
    "Basic recommenders just count what's bought together. Matrix factorization goes deeper: it "
    "learns *hidden tastes* from the purchase grid — a coffee-lover pattern, a tea-lover pattern — "
    "and uses them to fill the blanks, predicting what each customer would like but hasn't tried. "
    "It's the Netflix idea, and it needs nobody to label a single taste.",
)

matrix = mf.build_matrix(seed=42)
recon = mf.factorize(matrix, k=3)

st.markdown("### The purchase grid (customers × products)")
st.caption("Zeros are products not bought — the blanks the recommender tries to fill.")
st.dataframe(matrix.style.background_gradient(cmap="Blues", axis=None),
             use_container_width=True)

st.markdown("### Recommend for a customer")
user = st.selectbox("Pick a customer", list(matrix.index), index=2)
recs = mf.recommend(user, matrix, recon, n=2)

bought = [p for p in matrix.columns if matrix.loc[user, p] > 0]
st.write("**Has bought:** " + (", ".join(bought) if bought else "nothing yet"))
if recs and recs[0][1] > 0:
    top, score = recs[0]
    st.success(f"⭐ Top recommendation: **{top}** (predicted preference {score:.2f})")
    for p, s in recs[1:]:
        st.write(f"• {p} — {s:.2f}")
    st.caption("Notice the model recommends items that fit the customer's *taste cluster*, "
               "not just the single most popular product overall.")
else:
    st.info("This customer's tastes are already well covered — nothing strongly predicted.")

with st.expander("What the model reconstructed (predicted preferences)"):
    st.dataframe(recon.style.background_gradient(cmap="Greens", axis=None),
                 use_container_width=True)

ui.leader_takeaway("Recommendations are among the highest-ROI uses of data — matrix factorization "
                   "predicts what a customer wants next from tastes it discovers on its own, no "
                   "manual tagging required.")
ui.footer()
