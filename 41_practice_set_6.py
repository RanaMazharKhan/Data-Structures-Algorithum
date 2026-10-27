# Practice set 6: a quick workout across everything learned so far
# Five short problems, one per idea: dynamic programming, bit tricks,
# two pointers, hash tables and greedy choices. Each solution is short
# on purpose, so read the comment above it first, then the code, then
# the printed answer.

# 1. Maximum subarray sum with Kadane's algorithm (DP in one pass)
# Keep the best sum ending at each position: either start fresh here,
# or extend the previous sum. The best of those is the answer.
def max_subarray(nums):
    best = current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best


print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6 (4, -1, 2, 1)


# 2. Missing number with XOR (bit manipulation)
# XOR cancels a number with itself, so XORing 0..n with the array
# leaves only the number that never appeared.
def missing_number(nums):
    missing = len(nums)
    for i, n in enumerate(nums):
        missing ^= i ^ n
    return missing


print(missing_number([3, 0, 1]))  # 2


# 3. Pair sum in a sorted array with two pointers
# One pointer at each end: if the sum is too big move the right one
# left, if too small move the left one right.
def pair_sum(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return []


print(pair_sum([1, 2, 4, 7, 11, 15], 18))  # [3, 4] (7 + 11 = 18)


# 4. First non-repeating character with a hash table
# Count every character once, then take the first one with count 1.
def first_unique(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


print(first_unique("leetcode"))  # 0 ('l')
print(first_unique("aabb"))       # -1 (none)


# 5. Climbing stairs with DP (Fibonacci in disguise)
# From each step you can climb 1 or 2, so ways(n) = ways(n-1) + ways(n-2).
def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


print(climb_stairs(5))  # 8

# ---
# Why it matters: practice sets are where separate topics start to
# connect. Spotting that a problem is "just a DP problem" or "just a
# two-pointer problem" is the skill interviews actually test.
