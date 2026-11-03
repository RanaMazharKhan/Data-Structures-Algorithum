# Practice set 13: mixed problems from all topics so far

# Problem 1: merge overlapping intervals with a greedy sort.
# Sort by start time, then keep extending the current interval
# whenever the next one overlaps it.
def merge_intervals(intervals):
    intervals = sorted(intervals)
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1, 6], [8, 10], [15, 18]]

# Problem 2: kth largest number with a heap.
# A min-heap of size k keeps the k largest numbers seen so far,
# and its top is the kth largest.
import heapq


def kth_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5

# Problem 3: longest substring without repeating characters (sliding window).
# Move the right end forward, and jump the left end past any repeated
# character so the window never holds a duplicate.
def longest_unique(s):
    seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best


print(longest_unique("abcabcbb"))  # 3 ("abc")
print(longest_unique("bbbbb"))     # 1

# Problem 4: count islands in a grid with BFS.
# An island is a group of connected 1s; flood-fill each one from
# its first cell and count how many flood-fills we start.
from collections import deque


def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = set()
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in seen:
                islands += 1
                queue = deque([(r, c)])
                seen.add((r, c))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols:
                            if grid[nx][ny] == 1 and (nx, ny) not in seen:
                                seen.add((nx, ny))
                                queue.append((nx, ny))
    return islands


print(count_islands([[1, 1, 0], [0, 1, 0], [0, 0, 1]]))  # 2

# Problem 5: climbing stairs with dynamic programming.
# To reach step n you come from step n-1 or n-2, so the number
# of ways is the sum of the ways to reach those two steps.
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


print(climb_stairs(5))  # 8

# Why it matters: real problems do not tell you which chapter they come from.
# Mixed practice trains you to spot the pattern - greedy, heap, sliding window,
# BFS or DP - and pick the right tool yourself.
