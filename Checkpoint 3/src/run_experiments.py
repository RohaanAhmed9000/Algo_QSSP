# driver that ties loader → LinSPP → validator

# src/run_experiments.py
"""
Driver: load ontology, sample cost, run linearization, validate.
"""
import random
import itertools
import networkx as nx
from src.graphine_loader import load_graphine_ontology
from src.sppm import linearizable
from src.apecp import apecp

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
    random.seed(42)

    # Running on "tao" inside the Graphine dataset
    ontology = 'data/Graphine/dataset/atmo'
    G, terms, defs = load_graphine_ontology(ontology)
    s, t = add_super_source_sink(G)
    d = 2

    # Sample random costs
    qd = {}
    # edges = list(G.edges())
    # for e in edges:
    #     qd[frozenset({e})] = random.uniform(-1, 1)
    # Sample random qd on all subsets of size d
    for combo in itertools.combinations(G.edges(), d):
        qd[frozenset(combo)] = random.uniform(-1, 1)
    # no quadratic terms for now
    is_lin, c = linearizable(G, s, t, qd, d)
    print('Linearizable:', is_lin)
    if is_lin:
        # print('Linearizing cost function:', c)
        print('  c(e) for each edge e:', c)
    else:
        print('Not linearizable')
    # Validate with APECP

    # Validate that all s->t paths have same cost β
    ok, beta = apecp(G, s, t, qd, d)
    print('APECP:', ok, 'β:', beta)
    if ok:
        # Check that all paths have the same cost
        for path in nx.all_simple_paths(G, s, t):
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            cost = sum(qd.get(frozenset(combo), 0.0) for combo in itertools.combinations(path_edges, d))
            print('Path:', path, 'Cost:', cost)
            assert abs(cost - beta) < 1e-8, "Path cost does not match β"
    else:
        print('Not all paths have the same cost')
