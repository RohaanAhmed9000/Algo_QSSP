def topological_sort(graph):
    visited = [0] * graph.n  # 0 = unvisited, 1 = visiting, 2 = visited
    stack = []

    def dfs(u):
        if visited[u] == 1:
            raise ValueError("Graph contains a cycle")
        if visited[u] == 2:
            return

        visited[u] = 1
        for v in graph.adj[u]:
            dfs(v)
        visited[u] = 2
        stack.append(u)

    for u in range(graph.n):
        if visited[u] == 0:
            dfs(u)

    return stack[::-1]
