# Kruskal's algorithm: build the cheapest network that connects everything

# A minimum spanning tree (MST) connects all nodes with the lowest
# possible total edge cost, using exactly n - 1 edges and no cycles.
# Kruskal's greedy idea: sort all edges by cost, then take each edge
# ONLY if it connects two different groups. Union-find tells us the
# groups and rejects any edge that would close a cycle.
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

# helper keeps the DSU inside kruskal so the demo below stays simple
def kruskal(n, edges):
    dsu = DSU(n)
    mst = []
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            mst.append((u, v, w))
            total += w
    return mst, total

# 6 towns, each edge is (town_a, town_b, cost of laying cable)
edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
         (2, 3, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]
mst, total = kruskal(6, edges)
print(mst)    # [(1, 2, 1), (1, 3, 2), (4, 5, 2), (0, 2, 3), (3, 5, 6)]
print(total)  # 14 - cheapest way to connect all 6 towns

# If the graph is disconnected, Kruskal returns a forest: fewer than
# n - 1 edges, one tree per connected component.
edges2 = [(0, 1, 5), (2, 3, 4)]
mst2, total2 = kruskal(4, edges2)
print(mst2, total2)   # [(2, 3, 4), (0, 1, 5)] 9 - two separate trees

# Kruskal's matters wherever you connect things cheaply: laying cable
# or roads between cities, designing computer networks, and clustering
# data points - it is the classic "cheapest way to connect everything".
