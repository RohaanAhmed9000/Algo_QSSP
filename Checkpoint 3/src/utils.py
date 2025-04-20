# topological sort, nonbasic‐arc selection, etc.

# src/utils.py
"""
Graph preprocessing utilities: topological orders, nonbasic arcs, pruning.
"""
import networkx as nx
from typing import Set, Tuple, Any

def prune_unreachable(G: nx.DiGraph, source: Any, sink: Any) -> nx.DiGraph:
    """Remove nodes/edges not on any source->sink path."""
    # TODO: implement forward/backward reachability
    pass

def topological_arc_order(G: nx.DiGraph) -> list:
    """Return a list of edges in a topological order respecting path direction."""
    # TODO: derive from node topo-order
    pass

def choose_nonbasic_arcs(G: nx.DiGraph, source: Any, sink: Any) -> Set[Tuple[Any,Any]]:
    """Select one outgoing arc per intermediate node to form in-tree rooted at sink."""
    # TODO: for each v != source, sink pick exactly one outgoing edge
    pass

def compute_strongly_basic_arcs(G: nx.DiGraph, nonbasic: Set[Tuple[Any,Any]], source: Any) -> Set[Tuple[Any,Any]]:
    """Return all edges not in nonbasic and not incident to the source."""
    # TODO: filter edges
    pass