# Practice set 23: mixed problems from all topics so far

# 1. Two Sum (hash table): store each number we have seen
# with its index, so for every new number we can check in
# O(1) whether its complement is already there.
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []

print("two sum [2, 7, 11, 15] target 9:", two_sum([2, 7, 11, 15], 9))

# 2. Longest Substring Without Repeating Characters (sliding
# window): keep a window with no duplicates. When a repeat
# appears, slide the left edge past the previous copy.
def longest_unique(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best

print("longest unique in 'abcabcbb':", longest_unique("abcabcbb"))

# 3. Shortest Path (Dijkstra): a heap always expands the
# closest unvisited city first, so the first time we pop a
# city its distance is final. Runs in O((V + E) log V).
import heapq

def dijkstra(graph, start):
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist

roads = {"A": [("B", 4), ("C", 2)], "B": [("D", 5)],
         "C": [("B", 1), ("D", 8)], "D": []}
print("shortest distances from A:", dijkstra(roads, "A"))

# 4. Valid Parentheses (stack): push every opening bracket.
# A closing bracket must match the top of the stack, and the
# stack must be empty at the end.
def is_valid(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack

print("is '([{}])' valid:", is_valid("([{}])"))
print("is '([)]' valid:", is_valid("([)]"))

# 5. Kth Largest Element (min-heap): keep a heap of the k
# biggest numbers seen so far. The heap root is always the
# kth largest, and each new number costs O(log k).
def kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

print("2nd largest in [3, 2, 1, 5, 6, 4]:", kth_largest([3, 2, 1, 5, 6, 4], 2))

# Practice sets matter because interviews rarely ask one topic in
# isolation: the skill is recognising which tool fits the problem,
# then writing it from scratch in minutes.
