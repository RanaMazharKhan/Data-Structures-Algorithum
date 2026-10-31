# Practice set 11: mixed problems from all topics so far

# Problem 1: two sum with a hash table.
# Find two numbers that add up to a target in one pass.
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return (seen[need], i)
        seen[num] = i
    return None


print(two_sum([2, 7, 11, 15], 9))  # (0, 1) because 2 + 7 = 9

# Problem 2: valid parentheses with a stack.
# Every closing bracket must match the most recent opening one.
def is_valid(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return len(stack) == 0


print(is_valid("()[]{}"))  # True
print(is_valid("([)]"))    # False

# Problem 3: kth largest element with a heap.
# Keep a min-heap of size k; its top is the kth largest so far.
import heapq


def kth_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5

# Problem 4: longest substring without repeating characters.
# Sliding window: move the left edge past the last repeat.
def longest_unique(s):
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


print(longest_unique("abcabcbb"))  # 3 ("abc")
print(longest_unique("bbbbb"))     # 1 ("b")

# Problem 5: count connected components with union-find.
# Union every edge, then count distinct roots.
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)


def components(n, edges):
    dsu = DSU(n)
    for a, b in edges:
        dsu.union(a, b)
    return len({dsu.find(i) for i in range(n)})


print(components(5, [(0, 1), (1, 2), (3, 4)]))  # 2

# Why it matters: interview and exam problems rarely announce their topic.
# Practising mixed sets trains you to recognise the right tool - hash table,
# stack, heap, sliding window or union-find - from the problem itself.
