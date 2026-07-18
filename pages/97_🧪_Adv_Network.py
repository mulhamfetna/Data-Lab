import pandas as pd
import streamlit as st

from workshop import network as nw, ui
from workshop.visuals import PALETTE

st.set_page_config(page_title="Network analysis", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Network analysis — influencers and hidden circles",
    "Referrals, transactions, follows — a lot of business is a network, and networks answer two "
    "questions tables can't: *who are the connectors* worth cultivating, and *which circles* form "
    "on their own (for targeting — or for spotting a fraud ring). We find both with no prior "
    "knowledge of how many circles exist.",
)

seed = st.slider("Shuffle the customer base", 1, 50, 42)
nodes, edges, adjacency, planted = nw.build_referral_graph(seed=seed)
labels = nw.detect_communities(nodes, adjacency, seed=0)
colors = {lbl: PALETTE[i % len(PALETTE)] for i, lbl in enumerate(sorted(set(labels.values())))}

st.markdown(f"### The referral network — {len(nodes)} customers, {len(edges)} referrals")
dot = ["graph { layout=neato; overlap=false; bgcolor=transparent; "
       "node[style=filled, shape=circle, width=0.3, label=\"\", color=\"#333\"];"]
for n in nodes:
    dot.append(f'{n} [fillcolor="{colors[labels[n]]}"];')
for a, b in edges:
    dot.append(f"{a} -- {b};")
dot.append("}")
st.graphviz_chart("\n".join(dot))
st.caption("Each colour is a community the algorithm found on its own. Notice the dense clusters "
           "with only a few links between them.")

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Most connected customers (influencers)**")
    deg = nw.degree_centrality(adjacency)
    top = pd.DataFrame([{"customer": f"#{n}", "connections": d}
                        for n, d in list(deg.items())[:5]])
    st.dataframe(top, hide_index=True, use_container_width=True)
with c2:
    st.markdown("**Communities found**")
    sizes = nw.community_sizes(labels)
    st.metric("Number of circles", len(sizes))
    st.bar_chart(pd.DataFrame({"circle": [f"C{i+1}" for i in range(len(sizes))],
                               "members": sorted(sizes.values(), reverse=True)}),
                 x="circle", y="members")

ui.leader_takeaway("Two network questions pay off fast: *who are the connectors* (reward them, "
                   "they spread your product) and *which clusters exist* (target them — or, in "
                   "fraud and risk, investigate them).")
ui.footer()
