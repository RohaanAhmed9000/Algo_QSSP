# APECPₖ solver (including the d=1 DP)

# src/apecp.py
"""
All-Paths-Equal-Cost Problem solver.
"""
import networkx as nx
from typing import Dict, Any, Tuple, FrozenSet
from src.sppm import linearizable

CostMap = Dict[FrozenSet[Tuple[Any, Any]], float]

def apecp(G: nx.DiGraph, source: Any, sink: Any,
          qd: CostMap, d: int) -> Tuple[bool, float]:
    """
    Returns (is_equal, beta) where is_equal=True iff every source->sink path P
    satisfies SPPd(P, qd)=beta, and beta is the common cost.
    """
    if d == 1:
        # dynamic programming: ensure all in-edges to each node have same reduced cost
        beta = None
        # cost[y] = cost of any path from source to y
        cost = {source: 0.0}
        for node in nx.topological_sort(G):
            if node == source:
                continue
            preds = list(G.predecessors(node))
            if not preds:
                return False, 0.0
            val = None
            for p in preds:
                e = frozenset({(p, node)})
                c = cost[p] + qd.get(e, 0.0)
                if val is None:
                    val = c
                elif abs(c - val) > 1e-8:
                    return False, 0.0
            cost[node] = val
        beta = cost[sink]
        return True, beta
    else:
        # reduce to linearization check
        is_lin, c = linearizable(G, source, sink, qd, d)
        # linearizable==source-beta iff all paths equal beta
        if not is_lin:
            return False, 0.0
        # check c assigns equal cost only to source-incidents
        # collect beta from any source->x arc
        betas = set(c[e] for e in G.edges(source))
        if len(betas) != 1:
            return False, 0.0
        beta = betas.pop()
        # ensure non-source arcs zero
        for u, v in G.edges():
            if u != source and abs(c.get((u, v), 0.0)) > 1e-8:
                return False, 0.0
        return True, beta
