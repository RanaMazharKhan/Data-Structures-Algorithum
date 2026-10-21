# Practice set 2: problems that mix heaps, DP, graphs, greedy and strings

# Top-k largest (heap): to find the k biggest numbers, keep a min-heap
# of size k. Push each number; when the heap grows past k, throw away
# the smallest. What stays are exactly the k largest. O(n log k).
import heapq

def top_k(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(heap, reverse=True)

print(top_k([5, 1, 9, 3, 7, 2, 8], 3))  # [9, 8, 7]

# Climbing stairs (DP): from step i you can climb 1 or 2 steps, so
# ways(i) = ways(i-1) + ways(i-2). That is the Fibonacci pattern.
# Build it bottom-up, keeping only the last two values.
def climb_stairs(n):
    a, b = 1, 1   # ways(0) = 1, ways(1) = 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(climb_stairs(5))   # 8 different ways up 5 steps

# Connected islands (graph DFS): count groups of '1's in a grid. Visit
# each land cell once with DFS, flood-filling its whole island, and
# count how many floods you had to start. O(rows * cols).
def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r < 0 or c < 0 or r >= rows or c >= cols or
                (r, c) in visited or grid[r][c] == '0'):
            return
        visited.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                islands += 1
    return islands

print(count_islands([
    ['1', '1', '0'],
    ['1', '0', '0'],
    ['0', '0', '1'],
]))  # 2 - one big island top-left, one single cell bottom-right

# Activity selection (greedy): pick the maximum number of non-overlapping
# meetings. Sort by FINISH time, then always take the earliest-finishing
# meeting that starts after the last one you took. Greedy is optimal here.
def max_activities(meetings):
    meetings = sorted(meetings, key=lambda m: m[1])  # sort by end time
    picked, last_end = 0, float('-inf')
    for start, end in meetings:
        if start >= last_end:
            picked += 1
            last_end = end
    return picked

print(max_activities([(1, 3), (2, 5), (4, 7), (6, 9)]))  # 2 meetings

# Anagram check (hash counting): two words are anagrams if every
# letter appears the same number of times in both. Count letters
# with a dictionary and compare.
def is_anagram(a, b):
    if len(a) != len(b):
        return False
    counts = {}
    for ch in a:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in b:
        if counts.get(ch, 0) == 0:
            return False
        counts[ch] -= 1
    return True

print(is_anagram("listen", "silent"))  # True
print(is_anagram("hello", "world"))    # False

# This set matters because these patterns show up everywhere: top-k in
# leaderboards, stairs-style DP in budgeting problems, island counting
# in image segmentation, greedy scheduling in calendars, and anagram
# checks in spellcheckers and plagiarism detection.
