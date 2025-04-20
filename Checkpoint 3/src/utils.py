# src/utils.py
"""
Graph preprocessing utilities: topological orders, nonbasic arcs, pruning.
"""
import networkx as nx
from typing import Set, Tuple, Any, List

def prune_unreachable(G: nx.DiGraph, source: Any, sink: Any) -> nx.DiGraph:
    """Remove nodes/edges not on any source->sink path."""
    # nodes reachable from source
    forward = set(nx.descendants(G, source)) | {source}
    # nodes that can reach sink (reverse graph)
    backward = set(nx.ancestors(G, sink)) | {sink}
    keep = forward & backward
    return G.subgraph(keep).copy()


def topological_arc_order(G: nx.DiGraph) -> List[Tuple[Any, Any]]:
    """Return a list of edges in a topological order respecting path direction."""
    topo_nodes = list(nx.topological_sort(G))
    # map node to position
    pos = {node: i for i, node in enumerate(topo_nodes)}
    # sort edges by tail pos then head pos
    edges = list(G.edges())
    edges.sort(key=lambda e: (pos[e[0]], pos[e[1]]))
    return edges


def choose_nonbasic_arcs(G: nx.DiGraph, source: Any, sink: Any) -> Set[Tuple[Any, Any]]:
    """Select one outgoing arc per intermediate node to form an in-tree rooted at sink."""
    # Reverse search: build tree of predecessors ending at sink
    nonbasic = set()
    # precompute nodes that reach sink
    reachable_to_sink = set(nx.ancestors(G, sink)) | {sink}
    # For each node v != source, choose exactly one outgoing arc in a DFS from sink backwards
    for v in G.nodes():
        if v == source or v == sink:
            continue
        # find one outgoing arc from v that leads closer to sink
        for _, w in G.out_edges(v):
            # ensure w can reach sink
            # if nx.has_path(G, w, sink):
            #     nonbasic.add((v, w))
            #     break
            if w in reachable_to_sink:
                nonbasic.add((v, w))
                break
    return nonbasic


def compute_strongly_basic_arcs(G: nx.DiGraph, nonbasic: Set[Tuple[Any, Any]], source: Any) -> Set[Tuple[Any, Any]]:
    """Return all edges not in nonbasic and not incident to the source."""
    return {(u, v) for u, v in G.edges() if (u, v) not in nonbasic and u != source}
