# Floyd-Warshall: all-pairs shortest paths via dynamic programming

# The idea: try every node k as a possible "middle" of the path.
# dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]). After the loop,
# dist[i][j] is the shortest path from i to j that may pass through
# any of the nodes. O(n^3) time, O(n^2) memory. Works with negative
# edges (but no negative cycles).
def floyd_warshall(graph):
    n = len(graph)
    INF = float('inf')
    dist = [[graph[i][j] for j in range(n)] for i in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


# Demo: 4 cities, directed roads (INF = no direct road).
INF = float('inf')
roads = [
    [0,    3,  INF, 7],    # city 0
    [8,    0,  2,   INF],  # city 1
    [5,    INF, 0,  1],    # city 2
    [2,    INF, INF, 0],    # city 3
]

result = floyd_warshall(roads)
for row in result:
    print(row)
# 0 -> 2 is 5 via city 1 (0->1->2), 1 -> 3 is 3 via city 2 (1->2->3),
# 3 -> 1 is 5 via city 0 (3->0->1). Direct roads were longer or absent.

# Detect a negative cycle: if dist[i][i] < 0 for some i, a negative
# cycle exists through node i (the algorithm's classic trick).
def has_negative_cycle(graph):
    dist = floyd_warshall(graph)
    return any(dist[i][i] < 0 for i in range(len(graph)))

print(has_negative_cycle(roads))  # False - no negative cycles here

# Small sanity check on a tiny graph.
print(floyd_warshall([[0, 1], [INF, 0]]))  # [[0, 1], [inf, 0]]

# Why it matters: whenever you need the shortest distance between
# EVERY pair (road networks, flight planners, network routing tables),
# one run of Floyd-Warshall beats running Dijkstra from each node.
