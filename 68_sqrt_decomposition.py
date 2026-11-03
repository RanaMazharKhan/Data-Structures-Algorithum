# Sqrt decomposition: range queries with block trick

# Split an array into blocks of about sqrt(n) elements and store
# each block's sum. A range sum then touches at most two partial
# blocks element by element, plus whole blocks in one step each.
# That is slower than a segment tree but far simpler to write.
import math


class SqrtDecomposition:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.block = int(math.sqrt(self.n)) or 1
        self.sums = [0] * ((self.n + self.block - 1) // self.block)
        for i, value in enumerate(self.arr):
            self.sums[i // self.block] += value

    # Point update: fix the element and its block sum.
    def update(self, index, value):
        self.sums[index // self.block] += value - self.arr[index]
        self.arr[index] = value

    # Range sum from left to right, inclusive.
    def query(self, left, right):
        total = 0
        while left <= right:
            if left % self.block == 0 and left + self.block - 1 <= right:
                total += self.sums[left // self.block]
                left += self.block
            else:
                total += self.arr[left]
                left += 1
        return total


nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sd = SqrtDecomposition(nums)
print(sd.query(0, 4))   # 15 (1 + 2 + 3 + 4 + 5)
print(sd.query(3, 8))   # 39 (4 + 5 + 6 + 7 + 8 + 9)
sd.update(2, 10)        # change 3 to 10
print(sd.query(0, 4))   # 22 (1 + 2 + 10 + 4 + 5)
print(sd.query(0, 9))   # 62, the whole array

# Why it matters: plain loops are O(n) per query and segment trees are
# more code. Sqrt decomposition is the middle ground - fast enough for
# most range queries, and simple enough to write correctly in an exam.
