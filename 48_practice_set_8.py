# Practice set 8: a quick workout across everything learned so far
# Five short problems, one per idea: hashing, two pointers, sliding
# window, dynamic programming and union-find. Each solution is short
# on purpose, so read the comment above it first, then the code, then
# the printed answer.

# 1. First non-repeating character with a hash table
# Count every character once, then return the first one whose
# count is exactly 1.
def first_unique(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in s:
        if counts[ch] == 1:
            return ch
    return None


print(first_unique("leetcode"))  # l


# 2. Merge two sorted lists with two pointers
# Always take the smaller front element, then move that pointer on.
def merge_sorted(a, b):
    i, j, out = 0, 0, []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]


print(merge_sorted([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]


# 3. Longest substring without repeating characters (sliding window)
# Grow the right end, and when a repeat appears, shrink the left
# end past the previous copy of that character.
def longest_unique(s):
    seen, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best


print(longest_unique("abcabcbb"))  # 3 ("abc")


# 4. Coin change: fewest coins to make an amount (DP)
# dp[x] is the fewest coins for amount x. For each coin, try using
# it last: dp[x] = 1 + dp[x - coin], keeping the smallest result.
def coin_change(coins, amount):
    dp = [999999] * (amount + 1)
    dp[0] = 0
    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x:
                dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != 999999 else -1


print(coin_change([1, 3, 4], 6))  # 2 (3 + 3)


# 5. Cycle detection in an undirected graph with union-find
# Join the ends of each edge. If both ends are already in the same
# set, that edge closes a cycle.
def has_cycle(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return True
        parent[ru] = rv
    return False


print(has_cycle(3, [(0, 1), (1, 2), (2, 0)]))  # True
print(has_cycle(3, [(0, 1), (1, 2)]))  # False

# ---
# Why it matters: practice sets are where separate topics start to
# connect. Spotting that a problem is "just a hash map problem" or
# "just a sliding window problem" is the skill interviews test.
