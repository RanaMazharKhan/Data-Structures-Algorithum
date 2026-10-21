# Practice set 1: small problems that mix arrays, strings, stack, queue and searching

# Two Sum (hash table trick): find two numbers in a list that add up to
# a target. Store each number's index as you go; for every new number
# check whether "target - number" was already seen. One pass, O(n).
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return (seen[target - num], i)
        seen[num] = i
    return None

print(two_sum([2, 7, 11, 15], 9))   # (0, 1) -> 2 + 7 = 9
print(two_sum([3, 2, 4], 6))        # (1, 2) -> 2 + 4 = 6

# Valid parentheses (stack): push opening brackets, pop when a closing
# one arrives and check it matches the opener. Anything left in the
# stack at the end means something never closed.
def valid_parentheses(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return len(stack) == 0

print(valid_parentheses("()[]{}"))   # True
print(valid_parentheses("([)]"))     # False - brackets crossed

# Binary search (divide and conquer): on a SORTED list, look at the
# middle. If the target is smaller, throw away the right half; if
# bigger, throw away the left half. Halving each step gives O(log n).
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9], 7))   # 3
print(binary_search([1, 3, 5, 7, 9], 6))   # -1 (not found)

# Merge two sorted lists (two pointers): walk both lists with one
# finger each, always take the smaller front element. This is the
# merge step that makes merge sort work.
def merge_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]  # append whatever ran out last

print(merge_sorted([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]

# Max subarray sum (Kadane's idea): walk once, keep the best sum ending
# at each position. If that running sum drops below 0, restart from 0
# because a negative start can never help the future.
def max_subarray(nums):
    best = current = nums[0]
    for num in nums[1:]:
        current = max(num, current + num)
        best = max(best, current)
    return best

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6 (4,-1,2,1)

# These problems matter because they are the "unit tests" of thinking
# like a programmer: every interview reuses these five patterns, and
# real code (autocomplete, spellcheck, search boxes) is built from them.
