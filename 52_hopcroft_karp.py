# Hopcroft-Karp: fast bipartite matching

# A bipartite graph has two groups (say workers and jobs) and edges only
# between groups, never inside one. A matching pairs up workers with jobs
# so no one is used twice. We want the maximum number of pairs.
# The simple approach finds one augmenting path at a time (slow). Hopcroft-Karp
# is faster: each round it finds a whole batch of shortest augmenting paths
# at once using BFS layers + DFS. It runs in O(E * sqrt(V)) instead of O(V*E).
# BFS builds layers of free (unmatched) left nodes; DFS then tries to extend
# each layer path to a free right node, flipping matches along the way.
from collections import deque


def hopcroft_karp(adj, n_left, n_right):
    # adj[u] = list of right-side nodes worker u can do
    INF = float("inf")
    pair_u = [-1] * n_left   # which job each worker is matched to
    pair_v = [-1] * n_right  # which worker each job is matched to
    dist = [0] * n_left

    def bfs():
        q = deque()
        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        found_free = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                pu = pair_v[v]
                if pu != -1 and dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
                if pu == -1:
                    found_free = True  # a free job is reachable
        return found_free

    def dfs(u):
        for v in adj[u]:
            pu = pair_v[v]
            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1 and dfs(u):
                matching += 1
    return matching, pair_u


# Example: 4 workers, 4 jobs. Worker 0 can do jobs 0,1; worker 1 job 0;
# worker 2 jobs 1,2,3; worker 3 job 2.
adj = [[0, 1], [0], [1, 2, 3], [2]]
size, pairs = hopcroft_karp(adj, 4, 4)
print("max matching size:", size)  # 4 - every worker gets a job
for worker, job in enumerate(pairs):
    if job != -1:
        print("worker", worker, "-> job", job)

# Why it matters: bipartite matching shows up everywhere - assigning
# workers to shifts, students to projects, or riders to orders - and
# Hopcroft-Karp is the standard fast way to solve it at scale.
