# Practice set 14: mixed problems from all topics so far

# Problem 1: shortest path in an unweighted graph with BFS.
# BFS visits neighbours level by level, so the first time we reach
# the target, we have used the fewest edges possible.
from collections import deque

graph = {0: [1, 2], 1: [3], 2: [3], 3: [4], 4: []}

def bfs_distance(start, target):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == target:
            return dist[node]
        for nxt in graph[node]:
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return -1

print(bfs_distance(0, 4))  # 3, path 0 -> 1 -> 3 -> 4

# Problem 2: longest common subsequence with DP.
# If the letters match we take both, otherwise we take the better
# of skipping one letter from either string.
def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[len(a)][len(b)]

print(lcs("abcde", "ace"))  # 3, the subsequence "ace"

# Problem 3: kth largest element using a heap.
# heapq is a min-heap, so keeping only k elements leaves the kth
# largest sitting at the top of the heap.
import heapq

def kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5

# Problem 4: are two nodes connected, using union-find.
# Union joins groups, find checks whether two nodes share a group.
parent = list(range(5))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    parent[find(a)] = find(b)

union(0, 1)
union(1, 2)
print(find(0) == find(2))  # True
print(find(0) == find(4))  # False

# Problem 5: count how many numbers are smaller than each element.
# Sorting once and using binary search is faster than comparing
# every pair, which is the whole point of the earlier lessons.
import bisect

nums = [8, 1, 2, 2, 3]
ordered = sorted(nums)
print([bisect.bisect_left(ordered, x) for x in nums])  # [4, 0, 1, 1, 3]

# Why it matters: real problems rarely say which topic they are.
# Practice sets train you to recognise the pattern first, then
# pick the right structure, instead of memorising one trick at a time.
