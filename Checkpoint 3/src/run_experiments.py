# driver that ties loader → LinSPP → validator

# src/run_experiments.py
"""
Driver: load ontology, sample cost, run linearization, validate.
"""
import random
import networkx as nx
from src.graphine_loader import load_graphine_ontology
from src.sppm import linearizable

def add_super_source_sink(G: nx.DiGraph):
    roots = [n for n in G if G.in_degree(n)==0]
    leaves = [n for n in G if G.out_degree(n)==0]
    G.add_node('super_source')
    G.add_node('super_sink')
    for r in roots:
        G.add_edge('super_source', r)
    for l in leaves:
        G.add_edge(l, 'super_sink')
    return 'super_source', 'super_sink'

if __name__ == '__main__':
    ontology = 'data/Graphine/dataset/tao'
    G, terms, defs = load_graphine_ontology(ontology)
    s, t = add_super_source_sink(G)
    d = 2
    # Sample random costs
    qd = {}
    edges = list(G.edges())
    for e in edges:
        qd[frozenset({e})] = random.uniform(-1, 1)
    # no quadratic terms for now
    is_lin, c = linearizable(G, s, t, qd, d)
    print('Linearizable:', is_lin)
    if is_lin:
        print('Linearizing cost function:', c)
