# Boruvka's algorithm: minimum spanning tree by parallel cheapest edges

# A minimum spanning tree (MST) connects all nodes with the lowest
# possible total edge cost, using exactly n - 1 edges and no cycles.
# Boruvka's idea is the oldest MST algorithm and the most parallel one:
# every component at once finds its own cheapest edge to another
# component, and all those edges are added in the same round. The
# components then merge, and the process repeats until one tree is left.
# Kruskal adds one edge at a time, Prim grows one tree - Boruvka grows
# many trees at the same time.
def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def boruvka(n, edges):
    parent = list(range(n))
    mst = []
    total = 0
    components = n
    while components > 1:
        # cheapest edge leaving each component, found in one scan
        cheapest = {}
        for u, v, w in edges:
            cu, cv = find(parent, u), find(parent, v)
            if cu == cv:
                continue
            if cu not in cheapest or w < cheapest[cu][2]:
                cheapest[cu] = (u, v, w)
            if cv not in cheapest or w < cheapest[cv][2]:
                cheapest[cv] = (u, v, w)
        # add every chosen edge at once, skipping ones that now
        # connect nodes already merged by an earlier edge this round
        added = 0
        for u, v, w in cheapest.values():
            cu, cv = find(parent, u), find(parent, v)
            if cu != cv:
                parent[cu] = cv
                mst.append((u, v, w))
                total += w
                components -= 1
                added += 1
        if added == 0:
            break  # graph is disconnected, no MST exists

    return mst, total

# 6 towns, each edge is (town_a, town_b, cost of laying cable)
# same graph as the Kruskal and Prim examples, so all answers match
edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
         (2, 3, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]
mst, total = boruvka(6, edges)
print(mst)    # [(0, 2, 3), (1, 2, 1), (1, 3, 2), (4, 5, 2), (3, 5, 6)]
print(total)  # 14 - same cheapest total as Kruskal's and Prim's

# each round at least halves the number of components, so Boruvka
# finishes in O(log n) rounds - that halving is why it is the
# natural choice when MSTs are computed in parallel
print(len(mst))  # 5 edges for 6 nodes, exactly n - 1

# Boruvka's matters wherever many pieces connect at once: parallel
# MST computation, clustering data points (each cluster grabs its
# nearest neighbour), and network design on distributed systems.
# It is also the ancestor of the modern parallel MST algorithms.
