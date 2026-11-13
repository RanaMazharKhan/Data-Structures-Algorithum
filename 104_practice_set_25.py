# Practice set 25: mixed problems from all topics so far

# 1. Min Stack: a stack that also reports its minimum in O(1).
# Keep a second stack of running minimums: push the new
# minimum alongside every value, pop them together.
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, x):
        self.stack.append(x)
        if not self.mins or x <= self.mins[-1]:
            self.mins.append(x)
        else:
            self.mins.append(self.mins[-1])

    def pop(self):
        self.mins.pop()
        return self.stack.pop()

    def get_min(self):
        return self.mins[-1]

ms = MinStack()
for x in [5, 2, 8, 1]:
    ms.push(x)
print("min after pushes:", ms.get_min())
ms.pop()
print("min after popping 1:", ms.get_min())

# 2. Next Greater Element (monotonic stack): scan from right
# to left, keeping a stack of candidates in decreasing order.
# The top is the next greater element; smaller values are
# popped because they can never be the answer for earlier
# numbers either.
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []
    for i in range(len(nums) - 1, -1, -1):
        while stack and stack[-1] <= nums[i]:
            stack.pop()
        if stack:
            result[i] = stack[-1]
        stack.append(nums[i])
    return result

print("next greater of [2, 1, 2, 4, 3]:", next_greater([2, 1, 2, 4, 3]))

# 3. Group Anagrams (hash table): anagrams share the same
# sorted letters, so the sorted word is a perfect hash key.
# All words with the same key land in one group.
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())

print("anagram groups:", group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

# 4. Word Break (DP): dp[i] is True when the first i letters
# can be split into dictionary words. Extend each reachable
# position by every word that matches there.
def word_break(s, words):
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(len(s)):
        if not dp[i]:
            continue
        for w in words:
            if s.startswith(w, i):
                dp[i + len(w)] = True
    return dp[len(s)]

print("can break 'leetcode' with [leet, code]:",
      word_break("leetcode", ["leet", "code"]))

# 5. Container With Most Water (two pointers): start with the
# widest pair and move the shorter wall inward, because only a
# taller wall can ever beat the current area.
def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, min(height[lo], height[hi]) * (hi - lo))
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best

print("max water for [1,8,6,2,5,4,8,3,7]:", max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))

# Practice sets matter because interviews rarely ask one topic in
# isolation: the skill is recognising which tool fits the problem,
# then writing it from scratch in minutes.
