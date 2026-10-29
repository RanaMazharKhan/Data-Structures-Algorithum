# Practice set 9: a quick workout across everything learned so far
# Five short problems, one per idea: greedy arrays, reversing,
# strings, shortest paths and dynamic programming. Each solution is
# short on purpose, so read the comment above it first, then the
# code, then the printed answer.

# 1. Maximum subarray sum with Kadane's algorithm
# Walk once, keeping the best sum of a subarray ending here. If
# that sum goes negative, drop it and restart from the next number.
def max_subarray(nums):
    best = current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best


print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6


# 2. Rotate an array right by k steps, in place, using reversals
# Reverse the whole array, then reverse each half separately, and
# the last k elements end up at the front in the right order.
def rotate(nums, k):
    k %= len(nums)
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])
    return nums


print(rotate([1, 2, 3, 4, 5], 2))  # [4, 5, 1, 2, 3]


# 3. Longest common prefix of a list of words
# The answer cannot be longer than the shortest word, and it must
# match every word character by character, so stop at the first
# mismatch.
def longest_prefix(words):
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
    return prefix


print(longest_prefix(["flower", "flow", "flight"]))  # fl


# 4. Shortest paths with Dijkstra on a small weighted graph
# Always settle the unvisited node with the smallest known distance
# first: once settled, no shorter route to it can appear later.
import heapq


def dijkstra(graph, start):
    dist = {node: 999999 for node in graph}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nxt, w in graph[node]:
            if d + w < dist[nxt]:
                dist[nxt] = d + w
                heapq.heappush(heap, (dist[nxt], nxt))
    return dist


graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
print(dijkstra(graph, 0))  # {0: 0, 1: 3, 2: 1, 3: 4}


# 5. Longest common subsequence length (DP table)
# dp[i][j] is the LCS length of the first i chars of a and first j
# of b. Equal chars add 1 to the diagonal, otherwise take the best
# of dropping a char from either string.
def lcs_length(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[len(a)][len(b)]


print(lcs_length("abcde", "ace"))  # 3 ("ace")

# ---
# Why it matters: practice sets are where separate topics start to
# connect. Spotting that a problem is "just a greedy scan" or "just
# a DP table" is the skill interviews actually test.
