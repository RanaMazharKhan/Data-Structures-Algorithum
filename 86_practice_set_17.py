# Practice set 17: mixed problems from everything so far

# Problem 1: valid parentheses - check if brackets close in the right order.
# A stack remembers the last opened bracket, so every closing bracket
# must match the top of the stack, otherwise the string is invalid.
def valid_parentheses(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack

print(valid_parentheses("({[]})"))  # True
print(valid_parentheses("([)]"))    # False - ] closes ( before [ is closed

# Problem 2: merge overlapping intervals into the fewest possible ranges.
# Sorting by start time first makes every overlap appear next to the
# interval it overlaps, so one pass can merge them greedily.
def merge_intervals(intervals):
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1, 6], [8, 10], [15, 18]]

# Problem 3: shortest paths from one node with Dijkstra's algorithm.
# A heap always expands the closest unvisited node first, so the first
# time a node is popped its distance is final and can never improve.
import heapq

def dijkstra(n, graph, start):
    dist = [float("inf")] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist

graph = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], []]
print(dijkstra(4, graph, 0))  # [0, 3, 1, 4] - 0->2->1->3 costs 4

# Problem 4: longest common subsequence of two strings.
# A table stores the best answer for every pair of prefixes; matching
# letters add one, different letters take the best of the two neighbours.
def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]

print(lcs("abcde", "ace"))  # 3 - the letters a, c and e appear in both

# Problem 5: search in a rotated sorted array.
# One half of the array is always sorted, so binary search first finds
# which half is sorted, then checks whether the target lies inside it.
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1

print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))  # 4
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 3))  # -1 - 3 is not there

# Practice sets matter because interviews mix topics: one problem needs
# a stack, the next a sort, the next a heap, the next a DP table.
# Recognizing the pattern fast is the real skill.
