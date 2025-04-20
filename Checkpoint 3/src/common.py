# src/common.py
"""
Common types and utilities shared between modules.
"""
import networkx as nx
from typing import Dict, Any, Tuple, FrozenSet
from itertools import combinations

CostMap = Dict[FrozenSet[Tuple[Any, Any]], float]

def sppd_cost(path_edges, qd, d):
    """
    Compute SPPd cost on a specific path (list of edges) by summing qd over all subsets up to size d.
    """
    cost = qd.get(frozenset(), 0.0)
    for k in range(1, d+1):
        for combo in combinations(path_edges, k):
            cost += qd.get(frozenset(combo), 0.0)
    return cost