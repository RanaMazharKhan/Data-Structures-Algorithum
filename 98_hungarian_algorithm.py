# Hungarian algorithm: minimum-cost assignment problem

# Given n workers and n jobs with a cost for each worker-job
# pair, assign every worker to a different job so the total
# cost is as small as possible. Trying all n! assignments is
# hopeless; the Hungarian algorithm solves it in O(n^3).
# The idea: keep a price (potential) for each worker and each
# job. A pair is "tight" when worker price + job price equals
# its cost. We grow a matching using only tight edges, and
# when we get stuck we adjust the prices so a new tight edge
# appears. When the matching covers everyone, it is optimal.

# Classic O(n^3) implementation (1-indexed internally, costs
# are given as a 0-indexed n x n matrix).
def hungarian(cost):
    n = len(cost)
    INF = float("inf")
    # u[i]: worker prices, v[j]: job prices, p[j]: worker matched
    # to job j, way[j]: previous job on the augmenting path
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        # Dijkstra-like search for the cheapest augmenting path
        # using only the reduced costs (cost - u - v)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0
            for j in range(1, n + 1):
                if used[j]:
                    continue
                cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                if cur < minv[j]:
                    minv[j] = cur
                    way[j] = j0
                if minv[j] < delta:
                    delta = minv[j]
                    j1 = j
            # adjust the prices so at least one new edge becomes tight
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        # flip the matching along the found augmenting path
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    # p[j] is the worker assigned to job j (1-indexed)
    assignment = [0] * n
    for j in range(1, n + 1):
        assignment[p[j] - 1] = j - 1
    total = sum(cost[i][assignment[i]] for i in range(n))
    return assignment, total

# cost[i][j]: what worker i charges for job j
cost = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4],
]
assignment, total = hungarian(cost)
print("assignment (worker -> job):", assignment)
for i, j in enumerate(assignment):
    print(" worker", i, "-> job", j, "cost", cost[i][j])
print("minimum total cost:", total)

# The Hungarian algorithm matters wherever one-to-one matching
# must be cheapest: assigning drivers to deliveries, workers to
# tasks, or players to positions, and it is the engine behind
# tracking objects across video frames.
