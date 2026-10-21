# Segment tree: answer range queries (sum/min/max) in O(log n) with point updates

# A segment tree stores the array as a binary tree. Each node covers a
# range: its left child covers the left half, right child the right
# half, and the node itself holds the aggregate (sum, min...) of the
# whole range. Updating one element touches O(log n) nodes; a range
# query merges O(log n) nodes, so both operations are O(log n).

# Build the tree as a flat list of size 4*n (safe upper bound) filled
# recursively: tree[node] = aggregate of tree[2*node] and tree[2*node+1].
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, l, r):
        if l == r:                       # leaf: a single element
            self.tree[node] = arr[l]
        else:
            mid = (l + r) // 2
            self._build(arr, 2 * node, l, mid)
            self._build(arr, 2 * node + 1, mid + 1, r)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    # Point update: set arr[idx] = val, then fix the ancestors up to the root.
    def update(self, idx, val, node=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if l == r:
            self.tree[node] = val
        else:
            mid = (l + r) // 2
            if idx <= mid:
                self.update(idx, val, 2 * node, l, mid)
            else:
                self.update(idx, val, 2 * node + 1, mid + 1, r)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    # Range sum query [ql, qr]: if a node is fully inside, take it;
    # if fully outside, contribute 0; otherwise combine both children.
    def query(self, ql, qr, node=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if ql > r or qr < l:             # no overlap
            return 0
        if ql <= l and r <= qr:          # full overlap
            return self.tree[node]
        mid = (l + r) // 2
        return (self.query(ql, qr, 2 * node, l, mid) +
                self.query(ql, qr, 2 * node + 1, mid + 1, r))

nums = [1, 3, 5, 7, 9, 11]
st = SegmentTree(nums)
print(st.query(1, 3))        # 15 -> 3 + 5 + 7
print(st.query(0, 5))        # 36 -> sum of everything
st.update(1, 10)             # change 3 to 10
print(st.query(1, 3))        # 22 -> 10 + 5 + 7

# A min-segment tree works the same way: store min() at each node
# instead of the sum. Try changing the combine step above to min()
# and see the query return the smallest value in a range.

# Segment trees matter because databases, analytics dashboards and game
# leaderboards constantly ask "what happened between date X and date Y?"
# while new events keep arriving. A segment tree answers that live.
