# Dinic's algorithm: maximum flow in a network

# A flow network has a source, a sink, and pipes with capacities.
# The max flow problem asks how much can be pushed from source to
# sink without breaking any pipe. Dinic's algorithm repeats two
# steps: build a level graph with BFS (each edge must go from one
# level to the next), then push as much flow as possible along it
# with DFS (a blocking flow), until the sink is unreachable.
# Each edge stores its reverse edge too, so flow pushed the wrong
# way earlier can be undone later.

from collections import deque


class Dinic:
    def __init__(self, n):
        self.graph = [[] for _ in range(n)]

    # Each edge is [to, reverse_index, remaining_capacity].
    def add_edge(self, fr, to, cap):
        forward = [to, cap, None]
        backward = [fr, 0, forward]
        forward[2] = backward
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    # BFS levels: level[v] is the shortest distance from the source.
    def _bfs(self, s, t, level):
        for i in range(len(level)):
            level[i] = -1
        level[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            for to, cap, rev in self.graph[v]:
                if cap > 0 and level[to] == -1:
                    level[to] = level[v] + 1
                    queue.append(to)
        return level[t] != -1

    # DFS pushes flow only forward through the level graph, and
    # lowers the capacity of used edges (raising the reverse edge).
    def _dfs(self, v, t, flow, level, it):
        if v == t:
            return flow
        while it[v] < len(self.graph[v]):
            edge = self.graph[v][it[v]]
            to, cap, rev = edge
            if cap > 0 and level[to] == level[v] + 1:
                pushed = self._dfs(to, t, min(flow, cap), level, it)
                if pushed:
                    edge[1] -= pushed
                    rev[1] += pushed
                    return pushed
            it[v] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        level = [0] * len(self.graph)
        while self._bfs(s, t, level):
            it = [0] * len(self.graph)
            while True:
                pushed = self._dfs(s, t, 10 ** 18, level, it)
                if not pushed:
                    break
                flow += pushed
        return flow


# Classic example network: source 0, sink 5, max flow is 23.
dinic = Dinic(6)
dinic.add_edge(0, 1, 16)
dinic.add_edge(0, 2, 13)
dinic.add_edge(1, 2, 10)
dinic.add_edge(1, 3, 12)
dinic.add_edge(2, 1, 4)
dinic.add_edge(2, 4, 14)
dinic.add_edge(3, 2, 9)
dinic.add_edge(3, 5, 20)
dinic.add_edge(4, 3, 7)
dinic.add_edge(4, 5, 4)
print(dinic.max_flow(0, 5))  # 23

# ---
# Why it matters: max flow models real networks - water pipes, road
# traffic, data through servers - and also solves bipartite matching
# and image segmentation, so it shows up far beyond textbook graphs.
