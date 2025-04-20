# core LinSPPₙ implementation

# src/sppm.py
"""
Linearization solver for SPPd (LinSPP_d) based on Çela et al. algorithm.
"""
import networkx as nx
from typing import Dict, Any, Tuple, Set, FrozenSet, List
from src.utils import (prune_unreachable, topological_arc_order,
                       choose_nonbasic_arcs, compute_strongly_basic_arcs)
from src.apecp import apecp

CostMap = Dict[FrozenSet[Tuple[Any,Any]], float]


def compute_gamma(G: nx.DiGraph, nonbasic: Set[Tuple[Any,Any]],
                  qd: CostMap, d: int) -> Dict[Tuple[FrozenSet, Any], float]:
    """
    Precompute gamma[B, x] = sum_{C subset N_x, |C|<=d-|B|} qd(B ∪ C).
    Returns gamma dict.
    """
    # build nonbasic-tree adjacency
    children: Dict[Any, List[Any]] = {}
    root = None
    for u, v in nonbasic:
        children.setdefault(v, []).append(u)
    # find sink as root (node with no outgoing nonbasic)
    all_nb = {u for u, _ in nonbasic} | {v for _, v in nonbasic}
    for v in G.nodes():
        if v not in all_nb or v not in {u for u, v in nonbasic}:
            root = v
            break
    gamma: Dict[Tuple[FrozenSet, Any], float] = {}
    # BFS from root backward
    order = list(nx.topological_sort(G))
    order.reverse()
    for x in order:
        Nx = _collect_nonbasic_subsets(x, nonbasic, G)
        for B_size in range(0, d):
            # iterate B across subsets of edges ending at x
            # for simplicity, we compute when needed in linearizable
            pass
    # Note: full implementation deferred
    return gamma


def linearizable(G: nx.DiGraph, source: Any, sink: Any,
                 qd: CostMap, d: int) -> Tuple[bool, Dict]:
    """
    Returns (is_lin, c) where c maps edge->cost if linearizable, else is_lin=False.
    """
    Gp = prune_unreachable(G, source, sink)
    N = choose_nonbasic_arcs(Gp, source, sink)
    gamma = compute_gamma(Gp, N, qd, d)
    c: Dict[Tuple[Any,Any], float] = {}
    # Solve APECP on each strongly basic arc
    for (u, v) in compute_strongly_basic_arcs(Gp, N, source):
        # build subgraph G(a)
        nodes_u = [n for n in Gp.nodes() if nx.has_path(Gp, source, n) and nx.has_path(Gp, n, u)]
        Ga = Gp.subgraph(nodes_u).copy()
        # derive qd-1 for arc a using gamma
        qa: CostMap = {}
        # TODO: fill qa from gamma
        ok, beta = apecp(Ga, source, u, qa, d-1)
        if not ok:
            return False, {}
        c[(u, v)] = beta
    # set costs for source-> nodes and nonbasics
    for (s, w) in Gp.edges(source):
        # cost = f({(s, w)} ∪ C) sum over C ⊆ N_w
        c[(s, w)] = sum(qd.get(frozenset({(s, w)} | set(C)), 0.0)
                        for C in _power_set([e for e in nonbasic if e[1]==w], d-1))
    for e in Gp.edges():
        if e not in c:
            c[e] = 0.0
    return True, c


def _collect_nonbasic_subsets(x, nonbasic, G):
    # placeholder: return list of nonbasic edges in subtree of x
    return []

def _power_set(edges: List[Tuple[Any,Any]], max_size: int):
    # generator of all subsets of edges up to max_size
    from itertools import combinations
    for r in range(0, max_size+1):
        for comb in combinations(edges, r):
            yield comb
