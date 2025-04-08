def dummy_cost_fn(path):
    # Simple quadratic-style cost: sum of node pairs
    return sum((i + 1) * (j + 1) for i, j in zip(path, path[1:]))
