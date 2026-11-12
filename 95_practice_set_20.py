# Practice set 20: mixed problems from all topics so far

# 1. Two Sum (hash table): for each number, check if its
# complement (target - x) was already seen. One pass, O(n).
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []

print("two sum:", two_sum([2, 7, 11, 15], 9))

# 2. Valid Parentheses (stack): push openers, pop and match
# closers. The stack must be empty at the end.
def valid_parentheses(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack

print("valid '()[]{}':", valid_parentheses("()[]{}"))
print("valid '([)]':", valid_parentheses("([)]"))

# 3. Merge Two Sorted Lists (linked list): walk both lists and
# always take the smaller head, like merging two sorted piles.
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def merge_lists(a, b):
    dummy = Node(0)
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

l1 = Node(1, Node(3, Node(5)))
l2 = Node(2, Node(4, Node(6)))
print("merged lists:", to_list(merge_lists(l1, l2)))

# 4. Binary Search (sorted array): halve the range each step
# until the target is found or the range is empty. O(log n).
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

print("binary search 7 in [1,3,5,7,9]:", binary_search([1, 3, 5, 7, 9], 7))

# 5. Shortest Path in an Unweighted Graph (BFS): expand level
# by level from the start, so the first time we reach a node
# we have the shortest route to it.
from collections import deque

def bfs_shortest(graph, start, goal):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            return dist[u]
        for v in graph.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return -1

graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C"]}
print("shortest A -> D:", bfs_shortest(graph, "A", "D"), "steps")

# Practice sets matter because interviews rarely ask one topic in
# isolation: the skill is recognising which tool fits the problem,
# then writing it from scratch in minutes.
