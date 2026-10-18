# Dijkstra's algorithm - the shortest path on a WEIGHTED graph

# BFS finds the fewest hops, but real roads have distances: a 2-hop
# detour can be shorter than a direct highway. Dijkstra handles this
# by always expanding the node with the smallest KNOWN distance so
# far, like a cautious explorer checking the cheapest route first.
import heapq   # gives us a ready-made min-heap (priority queue)

# Graph with weights: node -> {neighbor: distance}
roads = {
    "Home":    {"A": 4, "B": 2},
    "A":       {"Home": 4, "C": 3, "D": 10},
    "B":       {"Home": 2, "C": 5},
    "C":       {"A": 3, "B": 5, "D": 1},
    "D":       {"A": 10, "C": 1},
}

# Idea: keep a "best distance so far" for every node (infinity at
# first). Pop the unvisited node with the smallest distance, then try
# to improve each neighbor's distance through it. Once a node is
# popped, its distance is final - no shorter route can beat it.
def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}   # to rebuild the path later
    heap = [(0, start)]                     # (distance, node) pairs
    done = set()

    while heap:
        d, node = heapq.heappop(heap)       # cheapest unfinished node
        if node in done:
            continue
        done.add(node)
        for neighbor, w in graph[node].items():
            new_d = d + w
            if new_d < dist[neighbor]:
                dist[neighbor] = new_d     # found a cheaper way in
                prev[neighbor] = node
                heapq.heappush(heap, (new_d, neighbor))
    return dist, prev

distances, prev = dijkstra(roads, "Home")
print("shortest distances from Home:")
for node, d in distances.items():
    print(" ", node, "->", d)
# Home -> 0, A -> 4, B -> 2, C -> 7, D -> 8
# Home->A directly (4) beats Home->B->C->A (10);
# D is cheapest via C (Home->B->C->D = 2+5+1 = 8)


# Rebuild the actual route using the prev pointers
def shortest_path(prev, start, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = prev[node]
    path = path[::-1]
    return path if path[0] == start else None

print("route Home -> D:", shortest_path(prev, "Home", "D"))
# route Home -> D: ['Home', 'B', 'C', 'D']  (2 + 5 + 1 = 8)


# Edge weights must be non-negative - with negative roads the
# "cheapest popped node is final" promise breaks (use Bellman-Ford
# instead if negative weights exist).
# The heap makes it fast: each step costs log(n) instead of scanning
# every node for the minimum, so total time is O((nodes + edges) log n).

# Why it matters: this is literally Google Maps. Network routing,
# flight pricing, game AI pathfinding - any "cheapest way through a
# network" problem is Dijkstra (or a close cousin like A*).
