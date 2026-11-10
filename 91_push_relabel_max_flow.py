# Push-relabel algorithm: maximum flow with height labels

# Ford-Fulkerson finds one path at a time, which is slow when many
# paths share edges. Push-relabel works locally instead: every node
# gets a height, flow only runs downhill, and nodes with too much
# flow (excess) push it to lower neighbours. A node with excess but
# no lower neighbour is "relabelled" - lifted up - until its flow
# finds a way downhill again. No path search, just local pushes.
from collections import deque

def push_relabel(n, edges, source, sink):
    cap = [[0] * n for _ in range(n)]
    flow = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] += c
    height = [0] * n
    excess = [0] * n
    height[source] = n
    # preflow: flood every edge out of the source at full capacity
    for v in range(n):
        if cap[source][v]:
            flow[source][v] = cap[source][v]
            flow[v][source] = -cap[source][v]
            excess[v] = cap[source][v]
            excess[source] -= cap[source][v]

    def push(u, v):
        amount = min(excess[u], cap[u][v] - flow[u][v])
        flow[u][v] += amount
        flow[v][u] -= amount
        excess[u] -= amount
        excess[v] += amount

    def relabel(u):
        # lift u just above its lowest neighbour with spare capacity
        height[u] = 1 + min(height[v] for v in range(n)
                           if cap[u][v] - flow[u][v] > 0)

    # discharge each active node (excess > 0) until its excess is
    # gone: push downhill while possible, relabel when stuck
    active = deque([v for v in range(n)
                    if v != source and v != sink and excess[v] > 0])
    in_queue = [False] * n
    for v in active:
        in_queue[v] = True
    seen = [0] * n
    while active:
        u = active.popleft()
        in_queue[u] = False
        while excess[u] > 0:
            if seen[u] < n:
                v = seen[u]
                if cap[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                    push(u, v)
                    if v != source and v != sink and excess[v] > 0 and not in_queue[v]:
                        active.append(v)
                        in_queue[v] = True
                seen[u] += 1
            else:
                relabel(u)
                seen[u] = 0
    return -excess[source]

# the classic CLRS flow network, source 0, sink 5
edges = [(0, 1, 16), (0, 2, 13), (1, 2, 10), (1, 3, 12), (2, 1, 4),
         (2, 4, 14), (3, 2, 9), (3, 5, 20), (4, 3, 7), (4, 5, 4)]
print(push_relabel(6, edges, 0, 5))  # 23 - same answer as Dinic's

# a tiny network where the only path is a bottleneck
print(push_relabel(3, [(0, 1, 5), (1, 2, 3)], 0, 2))  # 3

# Push-relabel matters because it is the fastest max-flow method
# in practice: network routing, bipartite matching at scale, image
# segmentation (graph cuts), and anywhere Dinic's path-by-path
# search spends too long re-finding the same routes.
