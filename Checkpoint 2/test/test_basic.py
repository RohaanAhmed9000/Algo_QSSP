import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from linearization.graph import Graph
from linearization.linearizer import is_linearizable
from linearization.utils import dummy_cost_fn

def test_toy_graph():
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(1, 3)
    g.add_edge(0, 2)

    result = is_linearizable(g, dummy_cost_fn)
    print("Linearizable:", result)

def test_cycle_graph():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)  # Creates a cycle

    try:
        result = is_linearizable(g, dummy_cost_fn)
        print("Linearizable (Cycle Graph):", result)
    except Exception as e:
        print("Error (expected for cycle):", e)

def test_multiple_incoming():
    g = Graph(4)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    result = is_linearizable(g, dummy_cost_fn)
    print("Linearizable (Multiple Incoming):", result)

def test_disconnected_graph():
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(2, 3)

    try:
        result = is_linearizable(g, dummy_cost_fn)
        print("Linearizable (Disconnected Graph):", result)
    except Exception as e:
        print("Error (Disconnected Graph):", e)

def test_diamond_graph():
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)

    result = is_linearizable(g, dummy_cost_fn)
    print("Linearizable (Diamond Shape):", result)


if __name__ == "__main__":
    print("\n--- Test 1 ---")
    test_toy_graph()
    
    print("\n--- Test 2 ---")
    test_cycle_graph()
    
    print("\n--- Test 3 ---")
    test_multiple_incoming()
    
    print("\n--- Test 4 ---")
    test_disconnected_graph()
    
    print("\n--- Test 5 ---")
    test_diamond_graph()

