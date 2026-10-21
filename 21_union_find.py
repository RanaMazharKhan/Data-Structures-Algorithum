# Union-Find (Disjoint Set Union): merge groups and ask "are these two connected?"

# Union-Find keeps a family of groups that only ever MERGE. Two tricks
# make every operation almost O(1): path compression (find() flattens
# the chain by pointing every visited node straight at the root) and
# union by rank (always attach the shorter tree under the taller one,
# so trees stay shallow).
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # each node starts as its own group
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                    # already in the same group
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

uf = UnionFind(6)
uf.union(0, 1)
uf.union(2, 3)
print(uf.connected(0, 1))   # True - same group
print(uf.connected(0, 2))   # False - different groups
uf.union(1, 2)
print(uf.connected(0, 3))   # True - 1 joined the 2-3 group

# Kruskal's minimum spanning tree: connect all nodes with the cheapest
# possible set of edges. Sort edges by weight, then greedily take each
# edge ONLY if it connects two DIFFERENT groups (union() returns True).
# Taking a same-group edge would form a cycle.
def kruskal(n, edges):
    dsu = UnionFind(n)
    mst = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):  # cheapest first
        if dsu.union(u, v):       # different groups -> safe to take
            mst.append((u, v, w))
    return mst

# 5 towns, each edge is (town_a, town_b, cost of laying cable)
edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 5), (3, 4, 7)]
mst = kruskal(5, edges)
print(mst)                        # cheapest cable layout
print(sum(w for _, _, w in mst))  # 13 - minimum total cost

# Union-Find matters wherever things connect and merge: networks and
# friend groups, image segmentation (merging neighboring pixels of the
# same object), and building the cheapest road/cable/internet backbone.
