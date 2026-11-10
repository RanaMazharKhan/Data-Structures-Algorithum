# Practice set 18: mixed problems from everything so far

# Problem 1: two sum - find two numbers that add up to a target.
# A hash map remembers each number seen so far, so for every new
# number we only need one lookup for its complement (target - x).
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1] - 2 + 7 = 9

# Problem 2: kth largest element in an unsorted list.
# A min-heap of size k always holds the k biggest numbers seen so
# far, and its smallest element is the kth largest overall.
import heapq

def kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5

# Problem 3: detect a cycle in a linked list (Floyd's tortoise
# and hare). A fast pointer moving two steps and a slow pointer
# moving one step must meet inside a cycle, but never on a plain list.
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

a = Node(1); b = Node(2); c = Node(3)
a.next = b; b.next = c; c.next = b  # 3 points back to 2: a cycle
print(has_cycle(a))  # True
d = Node(1); d.next = Node(2); d.next.next = Node(3)
print(has_cycle(d))  # False - the list just ends

# Problem 4: number of islands in a grid of land (1) and water (0).
# Every unvisited land cell starts a new island, and a DFS floods
# the whole connected island so it is never counted twice.
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    def flood(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == "0":
            return
        grid[r][c] = "0"
        flood(r + 1, c); flood(r - 1, c); flood(r, c + 1); flood(r, c - 1)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                flood(r, c)
    return count

print(num_islands([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]))  # 2

# Problem 5: coin change - fewest coins that make an amount.
# A DP table stores the cheapest way to make every smaller amount,
# and each coin tries to improve the answer for amounts it can reach.
def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1

print(coin_change([1, 2, 5], 11))  # 3 - 5 + 5 + 1
print(coin_change([2], 3))  # -1 - 3 cannot be made from 2s

# Practice sets matter because interviews mix topics: one problem
# needs a hash map, the next a heap, the next two pointers, the
# next a DFS, the next a DP table. Recognizing the pattern fast
# is the real skill.
