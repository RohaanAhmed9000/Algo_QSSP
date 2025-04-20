# driver that ties loader → LinSPP → validator

# src/run_experiments.py
"""
Driver: load ontology, sample cost, run linearization, validate.
"""
import random
import networkx as nx
from src.graphine_loader import load_graphine_ontology
from src.sppm import linearizable

if __name__ == '__main__':
    # Example usage
    ontology = 'data/Graphine/dataset/tao'
    G, terms, defs = load_graphine_ontology(ontology)
    s, t = 'super_source', 'super_sink'
    # TODO: add super-source/sink to G if needed
    d = 2
    # Sample random quadratic costs on adjacent pairs
    qd = {}
    edges = list(G.edges())
    for e in edges:
        qd[frozenset([e])] = random.uniform(-1, 1)
    # TODO: sample pairwise costs up to d
    is_lin, c = linearizable(G, s, t, qd, d)
    print('Linearizable:', is_lin)
    if is_lin:
        print('Linearizing cost function:', c)