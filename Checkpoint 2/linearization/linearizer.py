from .graph import Graph
from .topo_sort import topological_sort
from .utils import dummy_cost_fn

def is_linearizable(graph, cost_fn):
    try:
        topo = topological_sort(graph)
    except ValueError as e:
        return False

    # Placeholder for local condition checks
    for v in topo:
        preds = graph.rev_adj[v]
        succs = graph.adj[v]
        for p1 in preds:
            for p2 in preds:
                for s1 in succs:
                    for s2 in succs:
                        # Avoid degenerate paths
                        if len({p1, p2, s1, s2}) < 4:
                            continue
                        lhs = cost_fn([p1, v, s1]) + cost_fn([p2, v, s2])
                        rhs = cost_fn([p1, v, s2]) + cost_fn([p2, v, s1])
                        if abs(lhs - rhs) > 1e-6:
                            return False
    return True
