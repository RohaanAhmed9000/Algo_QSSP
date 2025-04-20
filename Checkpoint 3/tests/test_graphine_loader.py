# tests/test_graphine_loader.py
"""
Test for graphine_loader: ensure graph structure and lists are read correctly.
"""
import pytest
import networkx as nx
from src.graphine_loader import load_graphine_ontology

def test_loader(tmp_path):
    # create fake ontology dir
    d = tmp_path / 'onto'
    d.mkdir()
    (d / 'name.txt').write_text("A\nB")
    (d / 'def.txt').write_text("defA\ndefB")
    # graph: A->B
    import json
    (d / 'graph.json').write_text(json.dumps({'B':['A']}))
    G, terms, defs = load_graphine_ontology(str(d))
    assert set(terms) == {'A','B'}
    assert defs == ['defA','defB']
    assert set(G.nodes()) >= {'A','B'}
    assert G.has_edge('A','B')