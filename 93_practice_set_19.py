# Practice set 19: mixed problems from everything so far

# Problem 1: longest substring without repeating characters.
# A sliding window with a set of seen letters: the right end grows,
# and when a letter repeats the left end moves past its last copy.
def longest_unique(s):
    seen = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best

print(longest_unique("abcabcbb"))  # 3 - "abc"
print(longest_unique("bbbbb"))     # 1 - only "b"
print(longest_unique("pwwkew"))    # 3 - "wke"

# Problem 2: merge overlapping intervals.
# Sort by start time, then walk through: if the next interval
# starts before the current one ends, stretch the current one.
def merge_intervals(intervals):
    intervals.sort()
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1, 6], [8, 10], [15, 18]]

# Problem 3: product of array except self, without division.
# One pass builds the product of everything to the left of each
# position, a second pass multiplies in everything to the right.
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out

print(product_except_self([1, 2, 3, 4]))  # [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))  # [0, 0, 9, 0, 0]

# Problem 4: maximum subarray sum (Kadane's algorithm).
# Walk once keeping the best sum of a subarray ending here: either
# extend the old subarray or start fresh at this number.
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6 - [4, -1, 2, 1]
print(max_subarray([5, 4, -1, 7, 8]))  # 23 - the whole array

# Problem 5: find the missing number from 0 to n with XOR.
# XOR of all numbers 0..n cancels out with XOR of the given numbers
# except the one that is missing, because x ^ x is always 0.
def missing_number(nums):
    miss = len(nums)
    for i, x in enumerate(nums):
        miss ^= i ^ x
    return miss

print(missing_number([3, 0, 1]))  # 2
print(missing_number([0, 1]))     # 2
print(missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))  # 8

# Practice sets matter because interviews mix topics: one problem
# needs a sliding window, the next sorting, the next two passes,
# the next a greedy scan, the next a bit trick. Recognizing the
# pattern fast is the real skill.
