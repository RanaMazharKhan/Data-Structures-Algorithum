# Sparse table: O(1) range queries after O(n log n) preprocessing

# A range query asks something about a slice of an array, like the
# minimum of arr[2:6]. Scanning the slice every time is O(n) per query.
# A sparse table precomputes answers for intervals of length 1, 2, 4, 8...
# so any query can be answered by combining two overlapping intervals.

class SparseTable:
    def __init__(self, arr):
        self.arr = arr
        n = len(arr)
        # log_table[i] = floor(log2(i)), used to pick the interval size
        self.log_table = [0] * (n + 1)
        for i in range(2, n + 1):
            self.log_table[i] = self.log_table[i // 2] + 1
        # st[k][i] = minimum of the interval of length 2^k starting at i
        k = self.log_table[n] + 1
        self.st = [[0] * n for _ in range(k)]
        self.st[0] = arr[:]
        j = 1
        while (1 << j) <= n:
            for i in range(n - (1 << j) + 1):
                # split the interval into two halves of length 2^(j-1)
                self.st[j][i] = min(self.st[j - 1][i],
                                    self.st[j - 1][i + (1 << (j - 1))])
            j += 1

    # minimum of arr[l:r] (r not included), in O(1) time
    def range_min(self, l, r):
        length = r - l
        j = self.log_table[length]
        # two overlapping intervals of length 2^j cover [l, r) fully
        return min(self.st[j][l], self.st[j][r - (1 << j)])


arr = [7, 2, 9, 4, 1, 8, 3, 6]
st = SparseTable(arr)
print(st.range_min(0, 4))  # 2 (min of 7, 2, 9, 4)
print(st.range_min(2, 6))  # 1 (min of 9, 4, 1, 8)
print(st.range_min(4, 8))  # 1 (min of 1, 8, 3, 6)
print(st.range_min(0, 8))  # 1 (min of the whole array)

# ---
# Why it matters: sparse tables answer range minimum/maximum queries in
# O(1) after one preprocessing pass, which is perfect when the array
# never changes and you have thousands of queries, like in LCA problems
# and competitive programming.
