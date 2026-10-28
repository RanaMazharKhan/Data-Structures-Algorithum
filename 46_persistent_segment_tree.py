# Persistent segment tree: versioned range queries with kth element

# A normal segment tree forgets its old state after an update, but
# sometimes you need every past version, like undo history in an
# editor or "what did the array look like after the first 3 edits?"
# A persistent segment tree keeps all versions: each update creates
# a new root, and only the O(log n) nodes on the updated path are
# copied, while every other node is shared with the previous version.
# So each version costs just O(log n) extra memory instead of a full
# copy of the array.

# Nodes are stored in three lists (left child, right child, count).
# Node 0 is the empty node: it points to itself and holds count 0.
# update(prev, l, r, p) returns the root of a new version where
# position p increased by 1, copying only the nodes on the path down.
# kth(root_left, root_right, l, r, k) finds the kth smallest value in
# the range between two versions: the count in the left child tells
# whether the answer is in the left half or the right half.

class PersistentSegTree:
    def __init__(self, size):
        self.left = [0]
        self.right = [0]
        self.count = [0]
        self.size = size

    def _new_node(self, left, right, count):
        self.left.append(left)
        self.right.append(right)
        self.count.append(count)
        return len(self.count) - 1

    # new version: add 1 at position p, based on version `prev`
    def update(self, prev, l, r, p):
        if l == r:
            return self._new_node(0, 0, self.count[prev] + 1)
        mid = (l + r) // 2
        if p <= mid:
            new_left = self.update(self.left[prev], l, mid, p)
            new_right = self.right[prev]
        else:
            new_left = self.left[prev]
            new_right = self.update(self.right[prev], mid + 1, r, p)
        return self._new_node(new_left, new_right,
                              self.count[prev] + 1)

    # kth smallest value between versions left_root (excluded) and
    # right_root (included), k is 1-based
    def kth(self, left_root, right_root, l, r, k):
        if l == r:
            return l
        mid = (l + r) // 2
        left_count = (self.count[self.left[right_root]]
                      - self.count[self.left[left_root]])
        if k <= left_count:
            return self.kth(self.left[left_root], self.left[right_root],
                            l, mid, k)
        return self.kth(self.right[left_root], self.right[right_root],
                        mid + 1, r, k - left_count)


# Build one version per prefix of the array: version[i] describes the
# first i elements, so the range [l, r] is version[r + 1] minus
# version[l]. Values are compressed to ranks 0..m-1 first, because
# the tree works on positions, not on the values themselves.
arr = [5, 1, 4, 2, 3]
sorted_values = sorted(set(arr))
rank = {value: i for i, value in enumerate(sorted_values)}
tree = PersistentSegTree(len(sorted_values))
versions = [0]  # version 0 is the empty array
for value in arr:
    versions.append(tree.update(versions[-1], 0,
                                len(sorted_values) - 1, rank[value]))

# kth smallest in the whole array [0, 4]: sorted is [1, 2, 3, 4, 5]
print(sorted_values[tree.kth(versions[0], versions[5], 0, 4, 1)])  # 1
print(sorted_values[tree.kth(versions[0], versions[5], 0, 4, 3)])  # 3
# kth smallest in subarray [1, 3] = [1, 4, 2], sorted [1, 2, 4]
print(sorted_values[tree.kth(versions[1], versions[4], 0, 4, 2)])  # 2
# old versions still work after newer ones exist: first 2 elements
print(sorted_values[tree.kth(versions[0], versions[2], 0, 4, 2)])  # 5

# ---
# Why it matters: versioned range queries power undo history, time
# travel in databases, and "kth smallest in a range" queries in
# competitive programming, all with only O(log n) new nodes per update.
