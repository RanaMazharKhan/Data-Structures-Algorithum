# Practice set 12: mixed problems from all topics so far

# Problem 1: first non-repeating character with a hash table.
# Count every character, then return the first one seen only once.
def first_unique(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in s:
        if counts[ch] == 1:
            return ch
    return None


print(first_unique("leetcode"))  # 'l'
print(first_unique("aabb"))      # None

# Problem 2: coin change with dynamic programming.
# dp[amount] is the fewest coins that make that amount, built up from smaller ones.
def coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


print(coin_change([1, 2, 5], 11))  # 3 (5 + 5 + 1)
print(coin_change([2], 3))         # -1, impossible

# Problem 3: shortest path in an unweighted graph with BFS.
# BFS visits nodes level by level, so the first time we reach the target
# we have used the fewest edges.
from collections import deque


def shortest_path(graph, start, target):
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        for neighbour in graph[node]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append((neighbour, dist + 1))
    return -1


graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
print(shortest_path(graph, "A", "D"))  # 2

# Problem 4: binary search on the answer with a sorted list.
# Find the first bad version: the earliest version that fails.
def first_bad(n, is_bad):
    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if is_bad(mid):
            right = mid
        else:
            left = mid + 1
    return left


print(first_bad(5, lambda v: v >= 4))  # 4

# Problem 5: longest palindromic substring by expanding around each centre.
# A palindrome reads the same both ways, so grow outwards from every centre.
def longest_palindrome(s):
    best = ""
    for centre in range(len(s)):
        for left, right in [(centre, centre), (centre, centre + 1)]:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                if right - left + 1 > len(best):
                    best = s[left:right + 1]
                left -= 1
                right += 1
    return best


print(longest_palindrome("babad"))  # "bab" (or "aba")
print(longest_palindrome("cbbd"))   # "bb"

# Why it matters: interview and exam problems rarely announce their topic.
# Practising mixed sets trains you to recognise the right tool - hash table,
# dynamic programming, BFS, binary search or two pointers - from the problem itself.
