# core LinSPPₙ implementation

# src/sppm.py
"""
Linearization solver for SPPd (LinSPP_d) based on Çela et al. algorithm.
"""
import networkx as nx
from typing import Dict, Any, Tuple, Set, FrozenSet, List
from src.utils import prune_unreachable, choose_nonbasic_arcs, compute_strongly_basic_arcs
from src.apecp import apecp
from itertools import combinations

CostMap = Dict[FrozenSet[Tuple[Any,Any]], float]


def sppd_cost(path_edges: List[Tuple[Any,Any]], qd: CostMap, d: int) -> float:
    """
    Compute SPPd cost on a specific path (list of edges) by summing qd over all subsets up to size d.
    """
    cost = qd.get(frozenset(), 0.0)
    for k in range(1, d+1):
        for combo in combinations(path_edges, k):
            cost += qd.get(frozenset(combo), 0.0)
    return cost


def linearizable(G: nx.DiGraph, source: Any, sink: Any,
                 qd: CostMap, d: int) -> Tuple[bool, Dict[Tuple[Any,Any], float]]:
    """
    Returns (is_lin, c) where c maps edge->cost if linearizable, else is_lin=False.
    """
    # prune unreachable parts
    Gp = prune_unreachable(G, source, sink)
    # pick nonbasic arcs
    N = choose_nonbasic_arcs(Gp, source, sink)
    c: Dict[Tuple[Any,Any], float] = {}

    # 1) Handle strongly basic arcs via APECP(d-1)
    for (u, v) in compute_strongly_basic_arcs(Gp, N, source):
        # # collect nodes between source and u
        # nodes_u = [n for n in Gp.nodes() if nx.has_path(Gp, source, n) and nx.has_path(Gp, n, u)]
        # Ga = Gp.subgraph(nodes_u).copy()
        # build subgraph of nodes reachable from source to u
        Ga = prune_unreachable(Gp, source, u)
        
        # build empty cost-map for order d-1 on Ga: APECP uses only its qd
        qa: CostMap = {}
        ok, beta = apecp(Ga, source, u, qa, d-1)
        if not ok:
            return False, {}
        c[(u, v)] = beta

    # 2) Precompute nonbasic-successor map for unique N_u paths
    N_map = {u: v for u, v in N}
    def get_Nu(u):
        path = []
        while u in N_map:
            v = N_map[u]
            path.append((u, v))
            u = v
        return path

    # 3) Compute costs for source arcs: c(a) = SPPd(a · N_w)
    for (src, w) in Gp.edges(source):
        path_edges = [(src, w)] + get_Nu(w)
        c[(src, w)] = sppd_cost(path_edges, qd, d)

    # 4) All other arcs (nonbasics) get zero
    for e in Gp.edges():
        if e not in c:
            c[e] = 0.0

    return True, c
