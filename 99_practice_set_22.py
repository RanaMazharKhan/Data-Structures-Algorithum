# Practice set 22: mixed problems from all topics so far

# 1. Count Words With a Prefix (trie): insert every word into
# a trie, then walk down the prefix and count the words in
# that subtree. Prefix queries become O(prefix length).
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0  # how many words pass through this node

def insert(root, word):
    node = root
    for ch in word:
        node = node.children.setdefault(ch, TrieNode())
        node.count += 1

def count_prefix(root, prefix):
    node = root
    for ch in prefix:
        if ch not in node.children:
            return 0
        node = node.children[ch]
    return node.count

root = TrieNode()
for w in ["apple", "app", "apply", "banana", "band"]:
    insert(root, w)
print("words starting with 'app':", count_prefix(root, "app"))
print("words starting with 'ban':", count_prefix(root, "ban"))

# 2. Connected Components (union-find): union every edge's
# endpoints, then count the distinct roots. Near O(1) per
# operation thanks to path compression and union by rank.
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1

dsu = DSU(6)
for a, b in [(0, 1), (1, 2), (3, 4)]:
    dsu.union(a, b)
print("connected components:", len({dsu.find(i) for i in range(6)}))

# 3. Range Sum Query (segment tree): build a tree where each
# node stores the sum of its range. A query adds up O(log n)
# nodes that exactly cover the range.
class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, lo, hi):
        if lo == hi:
            self.tree[node] = arr[lo]
            return
        mid = (lo + hi) // 2
        self._build(arr, node * 2, lo, mid)
        self._build(arr, node * 2 + 1, mid + 1, hi)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, node, lo, hi, ql, qr):
        if qr < lo or hi < ql:
            return 0
        if ql <= lo and hi <= qr:
            return self.tree[node]
        mid = (lo + hi) // 2
        return (self.query(node * 2, lo, mid, ql, qr)
                + self.query(node * 2 + 1, mid + 1, hi, ql, qr))

    def range_sum(self, l, r):
        return self.query(1, 0, self.n - 1, l, r)

st = SegTree([1, 3, 5, 7, 9, 11])
print("sum of [1..4]:", st.range_sum(1, 4))

# 4. Pattern Search (KMP): precompute the longest prefix that
# is also a suffix for each position, so a mismatch skips ahead
# instead of restarting the scan from scratch.
def kmp_search(text, pattern):
    # build the prefix table
    lps = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        lps[i] = j
    # scan the text
    hits = []
    j = 0
    for i, ch in enumerate(text):
        while j and ch != pattern[j]:
            j = lps[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            hits.append(i - j + 1)
            j = lps[j - 1]
    return hits

print("pattern 'ABABC' found at:", kmp_search("ABABDABACDABABCABAB", "ABABC"))

# 5. Course Schedule (topological sort): a course can be taken
# only after its prerequisites. Kahn's algorithm takes courses
# with no remaining prerequisites first; if some course is
# never taken, the prerequisites contain a cycle.
from collections import deque

def can_finish(num_courses, prereqs):
    graph = {i: [] for i in range(num_courses)}
    indegree = [0] * num_courses
    for course, pre in prereqs:
        graph[pre].append(course)
        indegree[course] += 1
    q = deque([i for i in range(num_courses) if indegree[i] == 0])
    taken = 0
    while q:
        u = q.popleft()
        taken += 1
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    return taken == num_courses

print("can finish 2 courses [[1, 0]]:", can_finish(2, [[1, 0]]))
print("can finish 2 courses [[1, 0], [0, 1]]:", can_finish(2, [[1, 0], [0, 1]]))

# Practice sets matter because interviews rarely ask one topic in
# isolation: the skill is recognising which tool fits the problem,
# then writing it from scratch in minutes.
