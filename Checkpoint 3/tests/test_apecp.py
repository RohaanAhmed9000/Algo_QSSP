# tests/test_apecp.py
"""
Unit tests for the APECP solver (d=1 and d>1 cases).
"""
import pytest
import networkx as nx
from src.apecp import apecp


def test_chain_uniform():
    # a -> b -> c with uniform costs
    G = nx.DiGraph()
    G.add_edge('a','b')
    G.add_edge('b','c')
    qd = {frozenset({('a','b')}): 1.0,
          frozenset({('b','c')}): 2.0}
    ok, beta = apecp(G, 'a', 'c', qd, 1)
    assert ok
    assert abs(beta - 3.0) < 1e-8


def test_chain_mismatch():
    # a -> b -> c with different costs still equal for each path
    G = nx.DiGraph()
    G.add_edge('a','b')
    G.add_edge('b','c')
    qd = {frozenset({('a','b')}): 1.0,
          frozenset({('b','c')}): 3.0}
    ok, beta = apecp(G, 'a', 'c', qd, 1)
    assert ok
    assert abs(beta - 4.0) < 1e-8


def test_fork_non_equal():
    # diamond a->b->d and a->c->d with mismatched edge costs
    G = nx.DiGraph()
    G.add_edge('a','b')
    G.add_edge('b','d')
    G.add_edge('a','c')
    G.add_edge('c','d')
    qd = {frozenset({('a','b')}): 1.0,
          frozenset({('b','d')}): 1.0,
          frozenset({('a','c')}): 1.0,
          frozenset({('c','d')}): 2.0}
    ok, beta = apecp(G, 'a', 'd', qd, 1)
    assert not ok


def test_simple_linearizable_d2():
    # small 2-edge path for d=2, no quadratic terms: trivially linearizable
    G = nx.DiGraph()
    G.add_edge('a','b')
    G.add_edge('b','c')
    # only linear costs
    qd = {
        frozenset({('a','b')}): 1.0,
        frozenset({('b','c')}): 2.0,
        frozenset(): 0.0
    }
    ok, beta = apecp(G, 'a', 'c', qd, 2)
    assert ok
    # beta should be sum of linear costs = 3.0
    assert abs(beta - 3.0) < 1e-8


if __name__ == '__main__':
    pytest.main()