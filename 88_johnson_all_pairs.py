# Johnson's algorithm: all-pairs shortest paths with reweighting

# Dijkstra is fast but cannot handle negative edges, and Bellman-Ford
# handles negatives but is slow when run from every node. Johnson's
# trick combines both: run Bellman-Ford once from a fake source to
# compute a "potential" for every node, then shift every edge weight
# so all weights become non-negative without changing which path is
# shortest. After that, Dijkstra from each node is safe and fast.
import heapq

INF = float("inf")

def bellman_ford(n, edges, start):
    dist = [INF] * n
    dist[start] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # a negative cycle exists, no shortest paths
    return dist

def dijkstra(n, graph, start):
    dist = [INF] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist

def johnson(n, edges):
    # a fake source with a 0-cost edge to every node lets
    # Bellman-Ford reach all of them and compute the potentials h
    extra = edges + [(n, v, 0) for v in range(n)]
    h = bellman_ford(n + 1, extra, n)
    if h is None:
        return None
    h = h[:n]
    # reweight: w'(u, v) = w + h[u] - h[v] is always >= 0, and
    # every u-to-v path is shifted by the same h[u] - h[v],
    # so the shortest path stays the shortest path
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w + h[u] - h[v]))
    all_pairs = []
    for s in range(n):
        d = dijkstra(n, graph, s)
        # undo the shift to get the true distances back
        all_pairs.append([d[v] - h[s] + h[v] if d[v] != INF else INF
                          for v in range(n)])
    return all_pairs

# 5 cities, some roads give a discount (negative weight) but no
# route loops back cheaper than it started (no negative cycle)
edges = [(0, 1, 3), (0, 2, 8), (0, 4, -4), (1, 4, 7), (1, 3, 1),
         (2, 1, 4), (3, 2, -5), (3, 0, 2), (4, 3, 6)]
result = johnson(5, edges)
for row in result:
    print(row)

# Johnson's matters wherever all-pairs distances are needed on a
# sparse graph with negative edges: road networks with toll rebates,
# currency arbitrage checks, and Johnson is what real routing
# libraries use instead of slow O(n^3) Floyd-Warshall on big maps.
