# Wavelet tree: kth smallest in a range

# Sorting a range for every query is slow. A wavelet tree splits the
# values in half again and again, like a binary search tree over the
# value range. Each node remembers, for each prefix, how many of its
# elements went left, so a query can walk down in logarithmic time.
class WaveletTree:
    def __init__(self, data, lo, hi):
        self.lo = lo
        self.hi = hi
        self.b = [0]
        self.left = None
        self.right = None
        if lo == hi or not data:
            return
        mid = (lo + hi) // 2
        left_data = []
        right_data = []
        for x in data:
            if x <= mid:
                left_data.append(x)
                self.b.append(self.b[-1] + 1)
            else:
                right_data.append(x)
                self.b.append(self.b[-1])
        self.left = WaveletTree(left_data, lo, mid)
        self.right = WaveletTree(right_data, mid + 1, hi)

    # kth smallest in data[l..r], with l and r 0-based and k 1-based.
    # Count how many elements of the range went left; if k fits in
    # that count, go left, otherwise go right with a smaller k.
    def kth(self, l, r, k):
        if self.lo == self.hi:
            return self.lo
        in_left = self.b[r + 1] - self.b[l]
        if k <= in_left:
            return self.left.kth(self.b[l], self.b[r + 1] - 1, k)
        return self.right.kth(l - self.b[l], r - self.b[r + 1], k - in_left)


arr = [3, 1, 4, 1, 5, 9, 2, 6]
wt = WaveletTree(arr, min(arr), max(arr))
print(wt.kth(0, 7, 1))  # 1, smallest of the whole array
print(wt.kth(0, 7, 4))  # 3, 4th smallest of the whole array
print(wt.kth(2, 5, 2))  # 4, 2nd smallest of [4, 1, 5, 9]
print(wt.kth(0, 3, 3))  # 3, 3rd smallest of [3, 1, 4, 1]

# Why it matters: ranking questions like "kth smallest salary in this
# department" or "median score in this range" come up in databases
# and statistics. A wavelet tree answers them without sorting the
# range again for every single query.
