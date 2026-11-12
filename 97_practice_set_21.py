# Practice set 21: mixed problems from all topics so far

# 1. K Largest Elements (heap): keep a min-heap of size k.
# Anything smaller than the heap's smallest is dropped, so
# after one pass the heap holds the k biggest values.
import heapq

def k_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(heap, reverse=True)

print("3 largest of [4, 1, 7, 3, 9, 2]:", k_largest([4, 1, 7, 3, 9, 2], 3))

# 2. Detect a Cycle in a Linked List (Floyd's tortoise and
# hare): a slow pointer moves one step, a fast one two steps.
# If they ever meet, the list has a cycle.
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

a = Node(1, Node(2, Node(3)))
a.next.next.next = a.next  # 3 points back to 2: a cycle
print("list has cycle:", has_cycle(a))
print("plain list has cycle:", has_cycle(Node(1, Node(2))))

# 3. Longest Substring Without Repeating Characters (sliding
# window): expand the right end, and when a character repeats,
# move the left end past its previous occurrence.
def longest_unique(s):
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best

print("longest unique in 'abcabcbb':", longest_unique("abcabcbb"))

# 4. Coin Change (DP): dp[i] is the fewest coins that make
# amount i. For each coin, try using it once more: dp[i] =
# min(dp[i], dp[i - coin] + 1).
def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1

print("fewest coins for 11 with [1, 2, 5]:", coin_change([1, 2, 5], 11))

# 5. Cheapest Path (Dijkstra): always expand the currently
# cheapest unvisited node, because no cheaper route to it
# can appear later. Works with weighted edges.
def dijkstra(graph, start):
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist

graph = {"A": [("B", 4), ("C", 2)], "B": [("D", 3)], "C": [("B", 1), ("D", 5)], "D": []}
print("cheapest costs from A:", dijkstra(graph, "A"))

# Practice sets matter because interviews rarely ask one topic in
# isolation: the skill is recognising which tool fits the problem,
# then writing it from scratch in minutes.
