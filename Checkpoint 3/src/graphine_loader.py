# src/graphine_loader.py
"""
Load Graphine dataset into a networkx DiGraph with name-definition mappings.
"""
import json
import networkx as nx
from typing import Tuple, List

def load_graphine_ontology(path: str) -> Tuple[nx.DiGraph, List[str], List[str]]:
    """
    Given the path to an ontology folder (containing name.txt, def.txt, graph.json),
    returns:
      - G: DiGraph where edges go from parent -> child
      - terms: list of terminology strings
      - definitions: list of definition strings (aligned with terms)
    """
    G = nx.DiGraph()
    # Load names and definitions
    with open(f"{path}/name.txt") as f:
        terms = [line.strip() for line in f if line.strip()]
    with open(f"{path}/def.txt") as f:
        definitions = [line.strip() for line in f if line.strip()]
    # Load graph structure
    with open(f"{path}/graph.json") as f:
        adj = json.load(f)
    # Build nodes and edges
    for term in terms:
        G.add_node(term)
    for child, parents in adj.items():
        # Some JSON entries may include nodes not in name.txt
        if child not in G:
            G.add_node(child)
        for p in parents:
            if p not in G:
                G.add_node(p)
            G.add_edge(p, child)
    return G, terms, definitions