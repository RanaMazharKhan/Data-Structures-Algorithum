# Centroid decomposition: divide and conquer on trees

# A centroid of a tree is a node that splits the tree into pieces
# that are all at most half the size of the whole tree. Removing it
# leaves small components, so we can solve a problem on each piece
# and combine the answers, just like merge sort splits an array.
# Repeating this on every component builds a "centroid tree" whose
# height is only O(log n), so walking up from any node to the root
# of the centroid tree visits very few nodes.

# First find subtree sizes with a simple depth-first search that
# ignores nodes already picked as centroids.
# Then walk down to the heavy child until no child subtree is
# bigger than half the tree: that node is the centroid.
class CentroidDecomposition:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        self.removed = [False] * n
        self.parent = [-1] * n
        self.size = [0] * n

    def _sizes(self, node, prev):
        self.size[node] = 1
        for nxt in self.adj[node]:
            if nxt != prev and not self.removed[nxt]:
                self._sizes(nxt, node)
                self.size[node] += self.size[nxt]

    def _find_centroid(self, node, prev, total):
        for nxt in self.adj[node]:
            if nxt != prev and not self.removed[nxt]:
                if self.size[nxt] > total // 2:
                    return self._find_centroid(nxt, node, total)
        return node

    # Pick the centroid, mark it removed, then decompose each
    # remaining component separately with this centroid as parent.
    def decompose(self, entry, parent_centroid):
        self._sizes(entry, -1)
        centroid = self._find_centroid(entry, -1, self.size[entry])
        self.parent[centroid] = parent_centroid
        self.removed[centroid] = True
        for nxt in self.adj[centroid]:
            if not self.removed[nxt]:
                self.decompose(nxt, centroid)
        return centroid


# Example tree: 0-1-2, 1-3, 3-4, 3-5-6
edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (5, 6)]
cd = CentroidDecomposition(7, edges)
root = cd.decompose(0, -1)
print(root)  # 3, the centroid of the whole tree
# parent[i] is the centroid above node i in the centroid tree
print(cd.parent)  # [1, 3, 1, -1, 3, 3, 5]
# Node 6 climbs 6 -> 5 -> 3, only 3 steps to the top, even though
# the original tree path from 6 to 0 is 5 edges long.

# ---
# Why it matters: centroid decomposition turns slow tree path queries
# (count nodes within distance k, nearest red node) into O(log n)
# steps per query, and it is a standard competitive programming tool.
