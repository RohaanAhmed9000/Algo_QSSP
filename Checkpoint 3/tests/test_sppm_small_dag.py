# tests/test_sppm_small_dag.py
"""
Test for basic linearizable call on tiny DAG.
"""
import networkx as nx
from src.sppm import linearizable

def test_trivial_linearizable():
    G = nx.DiGraph()
    G.add_edge('s','t')
    # linear cost only
    qd = {frozenset({('s','t')}): 5.0, frozenset(): 0.0}
    ok, c = linearizable(G, 's', 't', qd, 2)
    assert ok
    assert c.get(('s','t')) == 5.0


def test_simple_non_linearizable():
    G = nx.DiGraph()
    G.add_edge('s','u')
    G.add_edge('u','t')
    # add inconsistent quadratic cost
    qd = {
        frozenset({('s','u')}): 1.0,
        frozenset({('u','t')}): 2.0,
        frozenset({('s','u'),('u','t')}): -4.0,
        frozenset(): 0.0
    }
    # ok, _ = linearizable(G, 's', 't', qd, 2)
    # assert not ok
    ok, c = linearizable(G, 's', 't', qd, 2)
    # Only one path ⇒ always linearizable
    assert ok
    # Check that c(s,u)+c(u,t) == original SPP₂ cost (1+2−4 = −1)
    total = c[('s','u')] + c[('u','t')]
    assert abs(total - (1.0 + 2.0 - 4.0)) < 1e-8