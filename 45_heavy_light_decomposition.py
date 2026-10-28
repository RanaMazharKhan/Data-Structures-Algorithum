# Heavy-light decomposition: path queries on trees with a segment tree

# A path query on a tree (like "sum the values from node A to node B")
# is awkward because the path is not a flat array. Heavy-light
# decomposition (HLD) flattens the tree into an array: it cuts the tree
# into chains, where each chain is a downward run of "heavy" edges.
# A heavy edge is the edge from a node to its biggest subtree child.
# Every node belongs to exactly one chain, and any root-to-leaf path
# crosses only O(log n) chains, so a path query becomes a few fast
# segment-tree range queries instead of a slow walk.

# First pass: count subtree sizes and pick each node's heavy child,
# the child with the largest subtree. Second pass: walk down the heavy
# paths, giving every node a position in a flat array, and remember
# the head of each node's chain. A plain segment tree over that flat
# array then answers range sums in O(log n).

class SegmentTree:
    def __init__(self, data):
        n = 1
        while n < len(data):
            n *= 2
        self.n = n
        self.tree = [0] * (2 * n)
        for i, value in enumerate(data):
            self.tree[n + i] = value
        for i in range(n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    # point update: set position p to value
    def update(self, p, value):
        i = self.n + p
        self.tree[i] = value
        i //= 2
        while i:
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            i //= 2

    # range sum over [l, r]
    def query(self, l, r):
        l += self.n
        r += self.n
        total = 0
        while l <= r:
            if l % 2 == 1:
                total += self.tree[l]
                l += 1
            if r % 2 == 0:
                total += self.tree[r]
                r -= 1
            l //= 2
            r //= 2
        return total


class HLD:
    def __init__(self, adj, values, root=0):
        n = len(adj)
        self.parent = [-1] * n
        self.depth = [0] * n
        self.size = [0] * n
        self.heavy = [-1] * n
        self.head = [0] * n
        self.pos = [0] * n
        # first pass: sizes and heavy children, bottom-up
        order = []
        stack = [root]
        self.parent[root] = root
        while stack:
            v = stack.pop()
            order.append(v)
            for to in adj[v]:
                if to != self.parent[v]:
                    self.parent[to] = v
                    self.depth[to] = self.depth[v] + 1
                    stack.append(to)
        for v in reversed(order):
            self.size[v] = 1
            best = 0
            for to in adj[v]:
                if to != self.parent[v]:
                    self.size[v] += self.size[to]
                    if self.size[to] > best:
                        best = self.size[to]
                        self.heavy[v] = to
        # second pass: walk heavy paths first so each chain is contiguous
        cur = 0
        stack = [(root, root)]
        while stack:
            v, h = stack.pop()
            while v != -1:
                self.head[v] = h
                self.pos[v] = cur
                cur += 1
                # light children start new chains, handled later
                for to in adj[v]:
                    if to != self.parent[v] and to != self.heavy[v]:
                        stack.append((to, to))
                v = self.heavy[v]
        base = [0] * n
        for v in range(n):
            base[self.pos[v]] = values[v]
        self.seg = SegmentTree(base)

    # sum of values on the path from u to v
    def path_sum(self, u, v):
        total = 0
        # climb chain by chain until both nodes share one chain
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            total += self.seg.query(self.pos[self.head[u]], self.pos[u])
            u = self.parent[self.head[u]]
        # same chain now: the range between them is the rest of the path
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        total += self.seg.query(self.pos[u], self.pos[v])
        return total

    # change one node's value
    def update(self, v, value):
        self.seg.update(self.pos[v], value)


# Tree: 0 is the root, with children 1 and 2; 1 has children 3 and 4,
# 2 has child 5; 3 has child 6. Node values are just their labels + 1.
adj = [[1, 2], [0, 3, 4], [0, 5], [1, 6], [1], [2], [3]]
values = [1, 2, 3, 4, 5, 6, 7]
tree = HLD(adj, values)
print(tree.path_sum(6, 5))  # 7 + 4 + 2 + 1 + 3 + 6 = 23
print(tree.path_sum(3, 4))  # 4 + 2 + 5 = 11
tree.update(2, 10)
print(tree.path_sum(6, 5))  # 23 - 3 + 10 = 30

# ---
# Why it matters: path queries on trees appear in road networks,
# company hierarchies and game maps, and HLD turns each query into
# O(log^2 n) segment-tree work instead of an O(n) walk up the tree.
