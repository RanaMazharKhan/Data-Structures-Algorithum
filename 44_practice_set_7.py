# Practice set 7: a quick workout across everything learned so far
# Five short problems, one per idea: prefix sums, binary search,
# linked lists, graph search and greedy choices. Each solution is short
# on purpose, so read the comment above it first, then the code, then
# the printed answer.

# 1. Range sum in O(1) with prefix sums
# prefix[i] is the sum of the first i numbers, so the sum of any slice
# is just the difference of two prefix values.
def range_sum(nums, l, r):
    prefix = [0]
    for n in nums:
        prefix.append(prefix[-1] + n)
    return prefix[r] - prefix[l]


print(range_sum([2, 4, 1, 7, 3], 1, 4))  # 12 (4 + 1 + 7)


# 2. Search-insert position with binary search
# Halve the search range each step; the leftover position is where
# the target belongs, even if it is not in the list.
def search_insert(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


print(search_insert([1, 3, 5, 6], 5))  # 2 (already there)
print(search_insert([1, 3, 5, 6], 2))  # 1 (between 1 and 3)


# 3. Reverse a linked list by flipping pointers one by one
# Walk the list keeping the previous node, and point each node back
# at it instead of forwards.
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


def reverse(head):
    prev = None
    current = head
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


head = Node(1, Node(2, Node(3)))
print(to_list(reverse(head)))  # [3, 2, 1]


# 4. Count islands with depth-first search on a grid
# An island is a group of connected 1s. Flood-fill each one from its
# first cell, marking visited cells, and count how many fills you do.
def count_islands(grid):
    rows, cols = len(grid), len(grid[0])

    def flood(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return
        grid[r][c] = 0
        flood(r + 1, c)
        flood(r - 1, c)
        flood(r, c + 1)
        flood(r, c - 1)

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                flood(r, c)
                islands += 1
    return islands


print(count_islands([[1, 1, 0], [0, 1, 0], [0, 0, 1]]))  # 2


# 5. Maximum meetings with a greedy choice (activity selection)
# Sort by finish time and always take the earliest-finishing meeting
# that does not clash: it leaves the most room for the rest.
def max_meetings(meetings):
    meetings.sort(key=lambda m: m[1])
    count, last_end = 0, -1
    for start, end in meetings:
        if start >= last_end:
            count += 1
            last_end = end
    return count


print(max_meetings([(1, 3), (2, 4), (3, 5), (0, 6), (5, 7)]))  # 3

# ---
# Why it matters: practice sets are where separate topics start to
# connect. Spotting that a problem is "just a prefix-sum problem" or
# "just a greedy problem" is the skill interviews actually test.
