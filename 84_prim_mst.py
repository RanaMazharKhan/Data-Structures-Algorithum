# Prim's algorithm: minimum spanning tree with a priority queue

# A minimum spanning tree (MST) connects all nodes with the lowest
# possible total edge cost, using exactly n - 1 edges and no cycles.
# Prim's greedy idea: grow one tree from a starting node. Keep a
# heap of the cheapest edge that reaches each unvisited node, always
# add the cheapest one, and repeat until every node is in the tree.
# Unlike Kruskal's, Prim's grows one connected tree step by step.
import heapq

# adjacency list: graph[u] = list of (neighbour, cost) pairs
def prim(n, graph, start=0):
    visited = [False] * n
    heap = [(0, start, -1)]   # (cost, node, came_from)
    mst = []
    total = 0
    while heap:
        cost, u, parent = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        total += cost
        if parent != -1:
            mst.append((parent, u, cost))
        for v, w in graph[u]:
            if not visited[v]:
                heapq.heappush(heap, (w, v, u))
    return mst, total

# 6 towns, each edge is (town_a, town_b, cost of laying cable)
# same graph as the Kruskal example, so both answers should match
graph = [[] for _ in range(6)]
for u, v, w in [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
                (2, 3, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]:
    graph[u].append((v, w))
    graph[v].append((u, w))
mst, total = prim(6, graph)
print(mst)    # [(0, 2, 3), (2, 1, 1), (1, 3, 2), (3, 5, 6), (5, 4, 2)]
print(total)  # 14 - same cheapest total as Kruskal's

# the heap always holds the next cheapest way into the tree, so the
# smallest edge is picked in O(log n) time - that is why a priority
# queue is the heart of Prim's algorithm
print(len(mst))  # 5 edges for 6 nodes, exactly n - 1

# Prim's matters wherever you connect things cheaply: laying cable
# or roads between cities, designing computer networks, and clustering
# data points - use it when the graph is dense and you already have
# an adjacency list in hand.
