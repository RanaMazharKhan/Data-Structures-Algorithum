# Practice set 10: mixed problems from all topics so far

# Problem 1: Two Sum with a hash table.
# Given numbers and a target, find two indices that add up to it.
# Trick: while scanning, store each number seen; for x, check if target - x
# was already seen. One pass, O(n) time.
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], i)
        seen[x] = i
    return None


print(two_sum([2, 7, 11, 15], 9))   # (0, 1) because 2 + 7 = 9
print(two_sum([3, 2, 4], 6))        # (1, 2) because 2 + 4 = 6

# ---
# Problem 2: Valid parentheses with a stack (from file 01).
# Push opening brackets; a closing bracket must match the top of the stack.
def is_valid(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack


print(is_valid("()[]{}"))  # True
print(is_valid("(]"))      # False

# ---
# Problem 3: Maximum sum of k consecutive numbers - sliding window (file 09).
# Add the first k, then slide: subtract the number leaving, add the new one.
def max_sum_k(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


print(max_sum_k([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))  # 39 (4+2+10+23)
# Window sums: 17, 39, 38, 37, 27, 24 -> max is 39

# ---
# Problem 4: Shortest path in an unweighted graph - BFS (file 11).
# BFS visits level by level, so the first time we reach a node we used
# the fewest edges - that is the shortest path in an unweighted graph.
from collections import deque


def bfs_shortest(graph, start, goal):
    q = deque([(start, 0)])
    seen = {start}
    while q:
        node, d = q.popleft()
        if node == goal:
            return d
        for nb in graph[node]:
            if nb not in seen:
                seen.add(nb)
                q.append((nb, d + 1))
    return -1


graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
print(bfs_shortest(graph, "A", "D"))  # 2 (A -> B -> D)

# ---
# Problem 5: 0/1 knapsack with DP (file 14).
# dp[w] = best value achievable with capacity w. For each item, update
# capacities backwards so each item is used at most once.
def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7))  # 9 (items of weight 3 and 4)

# Why it matters: these five patterns - hash lookup, stack matching, sliding
# window, BFS levels, and DP tables - solve a huge share of interview and
# contest problems once you can spot which one fits.
