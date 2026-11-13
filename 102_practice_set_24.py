# Practice set 24: mixed problems from all topics so far

# 1. Merge Intervals (sorting + greedy): sort by start time,
# then walk through once, merging each interval into the last
# one whenever they overlap. Sorting dominates: O(n log n).
def merge_intervals(intervals):
    intervals.sort()
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

print("merged [[1,3],[2,6],[8,10],[15,18]]:",
      merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))

# 2. Number of Islands (BFS on a grid): count the land
# patches by flooding each one with BFS and marking visited
# cells, so each island is counted exactly once.
from collections import deque

def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            count += 1
            q = deque([(r, c)])
            grid[r][c] = "0"
            while q:
                x, y = q.popleft()
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                        grid[nx][ny] = "0"
                        q.append((nx, ny))
    return count

print("islands:", num_islands([["1", "1", "0"], ["0", "1", "0"], ["1", "0", "1"]]))

# 3. Coin Change (DP): dp[a] is the fewest coins that make
# amount a. For each coin, every amount from coin to target
# can improve: dp[a] = min(dp[a], dp[a - coin] + 1).
def coin_change(coins, amount):
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1

print("fewest coins for 11 with [1, 2, 5]:", coin_change([1, 2, 5], 11))

# 4. Search in Rotated Sorted Array (binary search): one half
# of a rotated sorted array is always sorted. Find which half
# is sorted, check if the target lies in it, and discard the
# other half, keeping O(log n) time.
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

print("search 0 in [4,5,6,7,0,1,2]:", search_rotated([4, 5, 6, 7, 0, 1, 2], 0))

# 5. Maximum Subarray (Kadane's algorithm): scan once, keeping
# the best sum of a subarray ending here. If that sum goes
# negative, drop it and restart at the next number.
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

print("max subarray of [-2,1,-3,4,-1,2,1,-5,4]:", max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))

# Practice sets matter because interviews rarely ask one topic in
# isolation: the skill is recognising which tool fits the problem,
# then writing it from scratch in minutes.
