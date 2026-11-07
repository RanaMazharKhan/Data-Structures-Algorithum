# Practice set 16: mixed problems from everything so far

# Problem 1: two sum - find two numbers that add to a target.
# A hash map remembers each number seen so far, so the partner
# (target - x) is found in O(1) instead of scanning the whole list.
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []

print(two_sum([2, 7, 11, 15], 9))   # [0, 1] because 2 + 7 = 9

# Problem 2: longest subarray with at most k zeros flipped to ones.
# Sliding window: grow the right end, and shrink the left end whenever
# the window holds more than k zeros.
def longest_ones(nums, k):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best

print(longest_ones([1, 1, 0, 1, 0, 0, 1, 1], 2))  # 5

# Problem 3: number of islands - count connected groups of 1s in a grid.
# DFS floods each island and marks it visited, so every island is
# counted exactly once.
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0

    def flood(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        flood(r + 1, c)
        flood(r - 1, c)
        flood(r, c + 1)
        flood(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                flood(r, c)
    return count

grid = [["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]
print(num_islands(grid))            # 2

# Problem 4: k-th smallest element using a heap.
# heapq.nsmallest keeps only the k smallest values, no full sort needed.
import heapq
print(heapq.nsmallest(3, [7, 10, 4, 3, 20, 15]))  # [3, 4, 7]

# Problem 5: check if a string is a palindrome, ignoring case and spaces.
# Two pointers walk in from both ends and must always match.
def is_palindrome(s):
    s = "".join(ch.lower() for ch in s if ch.isalnum())
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("A man a plan a canal Panama"))  # True

# Practice sets matter because interviews mix topics: one problem needs
# a hash map, the next a sliding window, the next a graph flood fill.
# Recognizing the pattern fast is the real skill.
