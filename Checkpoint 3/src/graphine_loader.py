# parse name, def, graph.json → networkx.DiGraph

# src/graphine_loader.py
"""
Load Graphine dataset into a networkx DiGraph with name-definition mappings.
"""
import json
import networkx as nx
from typing import Tuple, Dict, List

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
    name_file = f"{path}/name.txt"
    def_file = f"{path}/def.txt"
    with open(name_file) as f:
        terms = [line.strip() for line in f]
    with open(def_file) as f:
        definitions = [line.strip() for line in f]
    # Load graph structure
    with open(f"{path}/graph.json") as f:
        adj = json.load(f)
    # Build nodes and edges
    for term in terms:
        G.add_node(term)
    for child, parents in adj.items():
        for p in parents:
            G.add_edge(p, child)
    return G, terms, definitions