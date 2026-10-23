# Bellman-Ford - shortest paths even with negative edge weights
# Relax every edge V-1 times; if one more round still improves,
# a negative cycle exists (and shortest paths are impossible).

def bellman_ford(n, edges, start):
    # n = number of vertices, edges = list of (u, v, weight)
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0

    # relax: try to improve the path to v through edge u -> v
    for _ in range(n - 1):
        improved = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                improved = True
        if not improved:  # no changes, we are done early
            break

    # one extra round: any improvement means a negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return dist, True
    return dist, False


# Example: 5 cities, roads with costs (a discount is a negative weight)
edges = [(0, 1, 6), (0, 2, 7), (1, 2, 8), (1, 3, 5),
         (1, 4, -4), (2, 3, -3), (2, 4, 9), (3, 1, -2), (4, 0, 2), (4, 3, 7)]
dist, has_cycle = bellman_ford(5, edges, 0)
print("shortest distances from city 0:", dist)
print("negative cycle present?", has_cycle)

# ---
# Why it matters: Dijkstra fails on negative weights, Bellman-Ford
# handles them and spots negative cycles. Used in network routing
# (routing protocols) and detecting arbitrage in currency exchange.
