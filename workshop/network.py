"""Graph / network analysis — who connects to whom, and which clusters form.

Customers, referrals, suppliers, transactions — much of business is a *network*, and networks
answer questions tables can't: who are the influencers (most connected), and which communities
naturally cluster together (for targeting, or for spotting fraud rings). We build a referral
graph with a few planted circles, rank customers by how connected they are, and recover the
communities with **label propagation** — a simple, dependency-free clustering that needs no
prior knowledge of how many groups exist.
"""
from __future__ import annotations

from collections import Counter

import numpy as np

Adjacency = dict[int, set[int]]


def build_referral_graph(seed: int = 42, n_groups: int = 3, group_size: int = 9,
                         within: float = 0.55, between: float = 0.02):
    """A planted-community referral graph.

    Returns ``(nodes, edges, adjacency, planted)`` where ``planted[node]`` is the true group.
    Edges are dense within a group and rare between groups — the structure the detector should
    recover without being told it exists.
    """
    rng = np.random.default_rng(seed)
    nodes = list(range(n_groups * group_size))
    planted = {i: i // group_size for i in nodes}
    adjacency: Adjacency = {i: set() for i in nodes}
    edges: list[tuple[int, int]] = []
    for a in nodes:
        for b in nodes:
            if a >= b:
                continue
            p = within if planted[a] == planted[b] else between
            if rng.random() < p:
                adjacency[a].add(b)
                adjacency[b].add(a)
                edges.append((a, b))
    return nodes, edges, adjacency, planted


def degree_centrality(adjacency: Adjacency) -> dict[int, int]:
    """How many direct connections each node has — the simplest influence score."""
    return dict(sorted(((n, len(nbrs)) for n, nbrs in adjacency.items()),
                       key=lambda kv: kv[1], reverse=True))


def most_connected(adjacency: Adjacency) -> int:
    return next(iter(degree_centrality(adjacency)))


def detect_communities(nodes: list[int], adjacency: Adjacency,
                       seed: int = 0, iters: int = 30) -> dict[int, int]:
    """Label propagation: each node repeatedly adopts its neighbours' most common label."""
    rng = np.random.default_rng(seed)
    labels = {n: n for n in nodes}
    for _ in range(iters):
        order = list(nodes)
        rng.shuffle(order)
        changed = False
        for n in order:
            nbrs = adjacency[n]
            if not nbrs:
                continue
            counts = Counter(labels[m] for m in nbrs)
            top = max(counts.values())
            best = sorted(lbl for lbl, c in counts.items() if c == top)[0]
            if labels[n] != best:
                labels[n] = best
                changed = True
        if not changed:
            break
    return labels


def community_sizes(labels: dict[int, int]) -> dict[int, int]:
    return dict(Counter(labels.values()))
