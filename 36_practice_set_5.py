# Practice set 5: a quick workout across everything learned so far
# Five short problems, one per idea: stack, hash table, sliding window,
# heap and sorting. Each solution is short on purpose, so read the
# comment above it first, then the code, then the printed answer.

# 1. Balanced brackets with a stack
# Push every opener, pop on a closer, and the stack must end empty.
def balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack


print(balanced("({[]})"))   # True
print(balanced("([)]"))     # False


# 2. Two sum with a hash table
# Remember each number seen so far, so the partner is one lookup away.
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []


print(two_sum([2, 7, 11, 15], 9))   # [0, 1]


# 3. Longest substring without repeats, sliding window
# Slide the window's left edge past the last repeat of a character.
def longest_unique(s):
    last, start, best = {}, 0, 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best


print(longest_unique("abcabcbb"))   # 3 ("abc")


# 4. Kth largest with a heap
# heapq is a min-heap, so keep only the k biggest and read the top.
import heapq


def kth_largest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


print(kth_largest([3, 2, 1, 5, 6, 4], 2))   # 5


# 5. Merge overlapping intervals after sorting by start
# Sorting puts overlaps next to each other, so one pass merges them.
def merge(intervals):
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))   # [[1, 6], [8, 10], [15, 18]]

# ---
# Why it matters: practice sets are where separate topics start to
# connect. Spotting that a problem is "just a stack problem" or "just
# a hash table problem" is the skill interviews actually test.
