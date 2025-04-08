class Graph:
    def __init__(self, num_vertices):
        self.n = num_vertices
        self.adj = [[] for _ in range(self.n)]
        self.rev_adj = [[] for _ in range(self.n)]

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.rev_adj[v].append(u)

    def get_edges(self):
        return [(u, v) for u in range(self.n) for v in self.adj[u]]
