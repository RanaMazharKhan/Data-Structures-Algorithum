# Stoer-Wagner algorithm: global minimum cut of an undirected graph

# A minimum cut splits the graph into two parts so the total weight
# of the edges crossing the split is as small as possible. Stoer
# and Wagner's idea needs no source or sink: repeat a "maximum
# adjacency search" - grow a set by always adding the vertex most
# strongly connected to the set so far - and the last two vertices
# added give one candidate cut. Merge them, repeat, and the
# smallest candidate over all rounds is the global minimum cut.
def stoer_wagner(n, edges):
    # adjacency matrix: weights add up when vertices are merged
    w = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        w[u][v] += c
        w[v][u] += c
    alive = [True] * n
    best = float("inf")
    remaining = n
    while remaining > 1:
        # grow a set A: each step add the vertex with the largest
        # total weight to A (the "most tightly attached" vertex)
        in_a = [False] * n
        weights = [0] * n
        prev = -1
        for step in range(remaining):
            nxt = -1
            for v in range(n):
                if alive[v] and not in_a[v]:
                    if nxt == -1 or weights[v] > weights[nxt]:
                        nxt = v
            in_a[nxt] = True
            if step == remaining - 1:
                # the last vertex added and the one before it form
                # this round's cut: weight of the last vertex to A
                best = min(best, weights[nxt])
                # merge the last vertex into the previous one so
                # the next round works on a smaller graph
                for v in range(n):
                    w[prev][v] += w[nxt][v]
                    w[v][prev] += w[v][nxt]
                alive[nxt] = False
                remaining -= 1
                break
            prev = nxt
            for v in range(n):
                if alive[v] and not in_a[v]:
                    weights[v] += w[nxt][v]
    return best

# two tight clusters of 3 nodes joined by one weak link: cutting
# that single link is clearly the cheapest way to split the graph
edges = [(0, 1, 5), (1, 2, 5), (2, 0, 5),
         (3, 4, 5), (4, 5, 5), (5, 3, 5),
         (2, 3, 1)]
print(stoer_wagner(6, edges))  # 1 - the weak link is the min cut

# a square with a diagonal: the cheapest split cuts two edges
edges2 = [(0, 1, 2), (1, 2, 2), (2, 3, 2), (3, 0, 2), (0, 2, 3)]
print(stoer_wagner(4, edges2))  # 4

# Stoer-Wagner matters wherever the weakest split of a whole
# network is the question: finding the most fragile link in a
# power grid, splitting a community into two groups, or checking
# how easily a network can be disconnected.
