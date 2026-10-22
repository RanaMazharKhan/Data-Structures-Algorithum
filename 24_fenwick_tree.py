# Fenwick tree (BIT): range sum queries and point updates in O(log n)

# The idea: store partial sums in an array where each cell covers a
# power-of-two-sized range. Position i stores a range of length
# (i & -i) - the lowest set bit of i. Adding a value at index k means
# updating k, then jumping k += k & -k up the tree; a prefix sum means
# walking k -= k & -k back down. Both take O(log n).
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)  # 1-indexed, bit[0] unused

    def add(self, index, value):  # index is 0-based
        i = index + 1
        while i <= self.n:
            self.bit[i] += value
            i += i & -i

    def prefix_sum(self, index):  # sum of [0 .. index], 0-based
        total = 0
        i = index + 1
        while i > 0:
            total += self.bit[i]
            i -= i & -i
        return total

    def range_sum(self, left, right):  # sum of [left .. right]
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


# Demo: track daily sales, update one day, query totals and ranges.
sales = FenwickTree(7)
for day, amount in enumerate([40, 20, 10, 30, 50, 60, 25]):
    sales.add(day, amount)

print(sales.prefix_sum(6))       # 235 - total for the whole week
print(sales.range_sum(2, 4))     # 90  - days 2..4 (10+30+50)
sales.add(2, 5)                  # day 2 was undercounted: 10 -> 15
print(sales.range_sum(2, 4))     # 95  - updates propagate in O(log n)

# Why it matters: the go-to structure whenever you need "change one
# value, then ask for sums over ranges, over and over" - used in
# frequency counting, leaderboards, and order statistics problems.

# Quick sanity check against brute force on a random array.
import random
random.seed(7)
nums = [random.randint(0, 9) for _ in range(50)]
ft = FenwickTree(len(nums))
for i, v in enumerate(nums):
    ft.add(i, v)
ok = all(ft.range_sum(l, r) == sum(nums[l:r + 1])
         for l in range(50) for r in range(l, min(l + 5, 49)))
print(ok)  # True - every range matches the brute-force sum
