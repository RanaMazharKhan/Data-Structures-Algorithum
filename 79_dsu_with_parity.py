# DSU with parity: like union-find, but every node also remembers its xor to the root

# Plain DSU only tells you "same group or not". DSU with parity also
# remembers the xor (0 = same side, 1 = opposite side) from each node
# to its root. That one extra number lets us check constraints like
# "a and b must be different" or "xor of a and b must be w".
class DSUParity:
    def __init__(self, n):
        self.parent = list(range(n))
        self.xor_to_parent = [0] * n  # xor from node to its parent
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            root = self.find(self.parent[x])
            self.xor_to_parent[x] ^= self.xor_to_parent[self.parent[x]]
            self.parent[x] = root
        return self.parent[x]

    def xor_to_root(self, x):
        self.find(x)
        return self.xor_to_parent[x]

    # force xor(a, b) == w. Returns False if that contradicts earlier facts.
    def union(self, a, b, w):
        ra, rb = self.find(a), self.find(b)
        xa, xb = self.xor_to_parent[a], self.xor_to_parent[b]
        if ra == rb:
            return (xa ^ xb) == w     # already linked: just check consistency
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
            self.xor_to_parent[ra] = xa ^ xb ^ w
        else:
            self.parent[rb] = ra
            self.xor_to_parent[rb] = xa ^ xb ^ w
            if self.rank[ra] == self.rank[rb]:
                self.rank[ra] += 1
        return True

    def xor(self, a, b):
        if self.find(a) != self.find(b):
            return None               # no relation known yet
        return self.xor_to_parent[a] ^ self.xor_to_parent[b]

# xor constraints: "x xor y = 1" means x and y are different
dsu = DSUParity(5)
print(dsu.union(0, 1, 1))   # True - 0 and 1 are different
print(dsu.union(1, 2, 0))   # True - 1 and 2 are the same
print(dsu.xor(0, 2))        # 1 - so 0 and 2 are different
print(dsu.union(0, 2, 0))   # False - contradicts: 0 xor 2 is 1, not 0

# Bipartite check: an edge means its ends must be on opposite sides
# (xor = 1). If adding an edge contradicts, the graph is not bipartite.
def is_bipartite(n, edges):
    dsu = DSUParity(n)
    for u, v in edges:
        if not dsu.union(u, v, 1):
            return False
    return True

print(is_bipartite(4, [(0, 1), (1, 2), (2, 3), (3, 0)]))  # True - a square
print(is_bipartite(3, [(0, 1), (1, 2), (2, 0)]))          # False - a triangle

# DSU with parity matters for bipartite checks, xor equations, and
# "enemy/friend" puzzles: any problem where two things must be equal
# or opposite, and you learn the rules one by one.
