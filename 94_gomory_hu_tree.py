# Gomory-Hu tree: all-pairs minimum cuts in one tree

# A min cut between two vertices is the cheapest set of edges whose
# removal separates them. A Gomory-Hu tree packs the min cut for
# EVERY pair into a single tree: the min cut between any two vertices
# is simply the smallest edge on the path between them in the tree.
# The trick (Gusfield's method): start with all vertices in one
# group, pick two vertices in the same group, find their min cut,
# split the group, and keep going. Only n - 1 max-flow runs are
# needed instead of one for every pair.

# Edmonds-Karp max flow, which also tells us which vertices stay
# on the source side of the min cut (the ones reachable in the
# leftover residual graph after the flow stops).
from collections import deque

def min_cut(n, edges, s, t):
    # residual capacities, built fresh for every run
    cap = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] += c
        cap[v][u] += c
    flow = 0
    while True:
        # BFS for a path from s to t with leftover capacity
        parent = [-1] * n
        parent[s] = s
        q = deque([s])
        while q and parent[t] == -1:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    q.append(v)
        if parent[t] == -1:
            break
        # push the bottleneck amount along the found path
        amount = float("inf")
        v = t
        while v != s:
            amount = min(amount, cap[parent[v]][v])
            v = parent[v]
        v = t
        while v != s:
            cap[parent[v]][v] -= amount
            cap[v][parent[v]] += amount
            v = parent[v]
        flow += amount
    # vertices still reachable from s are the source side of the cut
    seen = [False] * n
    seen[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        for v in range(n):
            if not seen[v] and cap[u][v] > 0:
                seen[v] = True
                q.append(v)
    return flow, seen

# Build the tree: parent[i] is i's parent in the tree and weight[i]
# is the min cut value of the edge between i and its parent.
def gomory_hu_tree(n, edges):
    parent = [0] * n
    weight = [0] * n
    for s in range(1, n):
        t = parent[s]
        cut, side = min_cut(n, edges, s, t)
        # vertices in t's old group that lie on s's side of the
        # cut now hang under s instead of t
        for i in range(n):
            if i != s and parent[i] == t and side[i]:
                parent[i] = s
        # if t's parent is on s's side, s and t swap places so the
        # tree stays connected; the old edge weight moves with s
        if side[parent[t]]:
            parent[s] = parent[t]
            parent[t] = s
            weight[s] = weight[t]
            weight[t] = cut
        else:
            weight[s] = cut
    return [(i, parent[i], weight[i]) for i in range(1, n)]

# The min cut between two vertices is the smallest tree edge on
# the path between them, so climb both vertices up to their
# lowest common ancestor and take the smallest edge met.
def tree_min_cut(tree, a, b):
    parent = {}
    edge_w = {}
    for u, v, w in tree:
        parent[u] = v
        edge_w[u] = w
    def ancestors(x):
        chain = []
        while x in parent:
            chain.append(x)
            x = parent[x]
        chain.append(x)  # the root
        return chain
    ca, cb = ancestors(a), ancestors(b)
    # lowest common ancestor: first node of a's chain found in b's
    lca = next(x for x in ca if x in cb)
    weights = []
    for x in ca:
        if x == lca:
            break
        weights.append(edge_w[x])
    for x in cb:
        if x == lca:
            break
        weights.append(edge_w[x])
    return min(weights)

# a small network: two tight groups joined by a couple of links
edges = [(0, 1, 4), (0, 2, 3), (1, 2, 2),
         (1, 3, 5), (2, 3, 1), (2, 4, 6), (3, 4, 2)]
tree = gomory_hu_tree(5, edges)
print("Gomory-Hu tree edges (u, v, min cut):")
for e in tree:
    print(" ", e)

# check the tree against plain max flow for a few pairs
for a, b in [(0, 3), (0, 4), (1, 4)]:
    direct, _ = min_cut(5, edges, a, b)
    print("min cut", a, "-", b, ":", tree_min_cut(tree, a, b),
          "(max flow says", direct, ")")

# A Gomory-Hu tree matters wherever every pair's weakest link is
# needed at once: finding the most fragile connections in a
# network, clustering data by how strongly parts are tied
# together, or planning which links to strengthen first.
