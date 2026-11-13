# Traveling salesman problem: Held-Karp DP over subsets

# A salesman must visit every city exactly once and return
# home, using the cheapest possible route. Trying all (n-1)!
# orders is hopeless, but DP over subsets is far better:
# dp[mask][i] is the cheapest cost of a tour that starts at
# city 0, visits exactly the cities in mask, and ends at i.
# To extend a tour we add one new city j: dp[mask | (1<<j)][j]
# = min over i of dp[mask][i] + dist[i][j]. With n cities there
# are 2^n masks and n endpoints, so the cost is O(n^2 * 2^n) -
# exponential, but it solves n = 15-20 easily while brute force
# already dies at n = 12.

def tsp(dist):
    n = len(dist)
    INF = float("inf")
    # dp[mask][i]: cheapest tour from 0 visiting mask, ending at i
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)) or dp[mask][i] == INF:
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                new_mask = mask | (1 << j)
                dp[new_mask][j] = min(dp[new_mask][j],
                                      dp[mask][i] + dist[i][j])
    # close the tour: return from the last city back to city 0
    full = (1 << n) - 1
    best = min(dp[full][i] + dist[i][0] for i in range(1, n))
    return best

# dist[i][j]: road distance between city i and city j
dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0],
]
print("cheapest tour cost:", tsp(dist))

# A bigger example: 5 cities on a line with a shortcut
dist5 = [
    [0, 2, 9, 10, 7],
    [2, 0, 6, 4, 3],
    [9, 6, 0, 8, 5],
    [10, 4, 8, 0, 6],
    [7, 3, 5, 6, 0],
]
print("cheapest tour cost (5 cities):", tsp(dist5))

# The same subset-DP idea powers delivery route planning,
# circuit-board drilling order and DNA sequencing, anywhere
# the cheapest way to visit every stop exactly once matters.
