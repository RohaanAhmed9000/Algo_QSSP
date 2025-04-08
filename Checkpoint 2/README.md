# Checkpoint 2: Linearization Algorithm

This repo contains basic infrastructure for experimenting with the linearization of quadratic and higher-order shortest path problems on DAGs.

## Files

- `graph.py`: Acyclic graph representation.
- `topo_sort.py`: Topological sort using DFS.
- `linearizer.py`: Checks linearizability via local two-path systems.
- `utils.py`: Placeholder cost functions.
- `test_basic.py`: Simple test to demonstrate functionality.

## How to Run

```bash
cd test
python3 test_basic.py
