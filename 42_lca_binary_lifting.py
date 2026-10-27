# LCA with binary lifting: lowest common ancestor in O(log n) per query

# The lowest common ancestor (LCA) of two nodes is the deepest node
# that is an ancestor of both, like the closest shared parent in a
# family tree. Walking up one parent at a time can take O(n) per query.
# Binary lifting precomputes jumps of size 1, 2, 4, 8... for every node,
# so any jump up the tree is a few big steps instead of many small ones.

# up[k][v] = the ancestor 2^k steps above v, built from up[k-1] twice:
# jumping 2^k up is two jumps of 2^(k-1) up. depth[v] is v's depth,
# found with one depth-first walk from the root.

class LCA:
    def __init__(self, children, root):
        n = len(children)
        max_log = n.bit_length()
        self.up = [[root] * n for _ in range(max_log)]
        self.depth = [0] * n
        # fill depth and the 1-step parents with a simple stack walk
        stack = [root]
        for v in stack:
            for child in children[v]:
                self.depth[child] = self.depth[v] + 1
                self.up[0][child] = v
                stack.append(child)
        # build the bigger jumps from the smaller ones
        for k in range(1, max_log):
            for v in range(n):
                self.up[k][v] = self.up[k - 1][self.up[k - 1][v]]

    # lift a node up by `steps` using its binary representation
    def lift(self, v, steps):
        k = 0
        while steps:
            if steps & 1:
                v = self.up[k][v]
            steps >>= 1
            k += 1
        return v

    # lowest common ancestor of u and v
    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # bring the deeper node up to the same depth first
        u = self.lift(u, self.depth[u] - self.depth[v])
        if u == v:
            return u
        # jump both up together, from big jumps down to small ones,
        # stopping just below their common ancestor
        for k in range(len(self.up) - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        return self.up[0][u]


# Tree: 0 is the root, 1 and 2 are its children, 3 and 4 hang under 1,
# 5 and 6 hang under 2. Children lists are in node-number order.
children = [[1, 2], [3, 4], [5, 6], [], [], [], []]
tree = LCA(children, 0)
print(tree.lca(3, 4))  # 1 (both under node 1)
print(tree.lca(3, 5))  # 0 (their paths meet only at the root)
print(tree.lca(5, 6))  # 2
print(tree.lca(3, 1))  # 1 (an ancestor of itself counts)

# ---
# Why it matters: LCA queries show up in tree problems, network routing
# and version control (finding a merge base), and binary lifting turns
# each query from a slow walk into a handful of jumps.
