# core LinSPPₙ implementation

# src/sppm.py
"""
Linearization solver for SPPd (LinSPP_d) based on Çela et al. algorithm.
"""
import networkx as nx
from typing import Dict, Any, Tuple, Set, FrozenSet
from src.utils import (prune_unreachable, topological_arc_order,
                       choose_nonbasic_arcs, compute_strongly_basic_arcs)
from src.apecp import apecp

# Type alias for cost functions over subsets of edges
CostMap = Dict[FrozenSet[Tuple[Any,Any]], float]


def compute_gamma(G: nx.DiGraph, nonbasic: Set, qd: CostMap, d: int) -> Dict:
    """
    Precompute gamma[B, x] = sum_{C subset N_x, |C|<=d-|B|} qd(B ∪ C).
    Returns nested dict gamma[(frozenset(B), x)] = float.
    """
    # TODO: tree-DP over nonbasic arcs
    pass


def linearizable(G: nx.DiGraph, source: Any, sink: Any,
                 qd: CostMap, d: int) -> Tuple[bool, Dict]:
    """
    Returns (is_lin, c) where c maps edge->cost if linearizable, else is_lin=False.
    """
    # Pre-pruning
    G = prune_unreachable(G, source, sink)
    N = choose_nonbasic_arcs(G, source, sink)
    gamma = compute_gamma(G, N, qd, d)
    # Solve APECP on each strongly basic arc
    c: Dict = {}
    for a in compute_strongly_basic_arcs(G, N, source):
        G_sub = G.subgraph([n for n in G.nodes if nx.has_path(G, source, n)]).copy()
        # TODO: build qd-1 for a using gamma
        is_eq, beta = apecp(G_sub, source, a[0], {}, d-1)
        if not is_eq:
            return False, {}
        c[a] = beta
    # TODO: fill in costs for source-arcs and nonbasics
    return True, c