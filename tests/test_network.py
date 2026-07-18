from collections import Counter

from workshop import network as nw


def test_graph_is_built_with_planted_groups():
    nodes, edges, adj, planted = nw.build_referral_graph(seed=42)
    assert len(nodes) == 27
    assert len(edges) > 0
    assert set(planted.values()) == {0, 1, 2}


def test_degree_centrality_sorted_and_complete():
    _n, _e, adj, _p = nw.build_referral_graph(seed=42)
    deg = nw.degree_centrality(adj)
    assert set(deg) == set(adj)
    vals = list(deg.values())
    assert vals == sorted(vals, reverse=True)


def test_most_connected_is_above_average():
    _n, _e, adj, _p = nw.build_referral_graph(seed=42)
    deg = nw.degree_centrality(adj)
    avg = sum(deg.values()) / len(deg)
    assert deg[nw.most_connected(adj)] >= avg


def test_communities_recover_planted_structure():
    nodes, _e, adj, planted = nw.build_referral_graph(seed=42)
    labels = nw.detect_communities(nodes, adj, seed=0)
    n_comm = len(set(labels.values()))
    assert 2 <= n_comm <= 8                        # finds structure, not 1 blob nor 27 singletons
    # purity: each planted group is mostly a single detected label
    pure = 0
    for g in set(planted.values()):
        members = [n for n in nodes if planted[n] == g]
        top = Counter(labels[n] for n in members).most_common(1)[0][1]
        pure += top
    assert pure / len(nodes) >= 0.7
