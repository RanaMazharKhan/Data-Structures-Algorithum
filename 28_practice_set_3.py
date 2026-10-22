# Practice set 3: problems that mix fenwick trees, all-pairs paths,
# topological order, string hashing, and earlier tools

# Inversion count (Fenwick): count pairs (i < j) with a[i] > a[j].
# Process right to left; the Fenwick tree holds the frequencies of
# values already seen, so each query "how many seen values are
# smaller than mine" is O(log n). Total O(n log n).
class FenwickTree:
    def __init__(self, n):
        self.bit = [0] * (n + 1)
    def add(self, i, v):
        i += 1
        while i < len(self.bit):
            self.bit[i] += v
            i += i & -i
    def prefix(self, i):  # count of values <= i
        total, i = 0, i + 1
        while i > 0:
            total += self.bit[i]
            i -= i & -i
        return total

def inversion_count(arr):
    vals = sorted(set(arr))
    rank = {v: i for i, v in enumerate(vals)}
    ft = FenwickTree(len(vals))
    inv = 0
    for x in reversed(arr):
        r = rank[x]
        inv += ft.prefix(r - 1)   # smaller values already to the right
        ft.add(r, 1)
    return inv

print(inversion_count([3, 1, 2]))        # 2 - (3,1) and (3,2)
print(inversion_count([1, 2, 3, 4]))     # 0 - already sorted

# Cheapest trip between any two stops (Floyd-Warshall): one run gives
# the cheapest fare between every pair of bus stops.
def cheapest_fares(stops, roads):
    INF = float('inf')
    dist = [[INF] * stops for _ in range(stops)]
    for i in range(stops):
        dist[i][i] = 0
    for u, v, cost in roads:
        dist[u][v] = min(dist[u][v], cost)
    for k in range(stops):
        for i in range(stops):
            for j in range(stops):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

fares = cheapest_fares(4, [(0, 1, 5), (1, 2, 3), (0, 2, 10), (2, 3, 1)])
print(fares[0][2], fares[0][3])  # 8 (via stop 1), 9 (via stops 1, 2)

# Course planner (topological sort, Kahn's): order courses so every
# prerequisite comes first; returns None if the schedule is impossible.
from collections import deque

def plan_courses(courses, prereqs):
    indeg = {c: 0 for c in courses}
    graph = {c: [] for c in courses}
    for pre, course in prereqs:  # pre must be taken before course
        graph[pre].append(course)
        indeg[course] += 1
    queue = deque([c for c in courses if indeg[c] == 0])
    order = []
    while queue:
        course = queue.popleft()
        order.append(course)
        for nxt in graph[course]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == len(courses) else None

print(plan_courses(['Math', 'Algo', 'ML', 'DB'],
                   [('Math', 'Algo'), ('Algo', 'ML'), ('Math', 'DB')]))
# Math first, then Algo, then ML and DB in either order

# Longest palindromic substring (DP, like KMP's window discipline):
# expand around every centre - odd and even lengths.
def longest_palindrome(s):
    best = ""
    for center in range(len(s)):
        for l, r in ((center, center), (center, center + 1)):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if r - l + 1 > len(best):
                    best = s[l:r + 1]
                l -= 1
                r += 1
    return best

print(longest_palindrome("babad"))  # "bab" (or "aba" - both correct)

# Pattern frequency (Rabin-Karp style rolling hash): count how often a
# word occurs in a paragraph without re-scanning each window.
def count_occurrences(text, pattern):
    base, mod = 256, 10**9 + 7
    n, m = len(text), len(pattern)
    if m > n:
        return 0
    high = pow(base, m - 1, mod)
    ph, wh = 0, 0
    for i in range(m):
        ph = (ph * base + ord(pattern[i])) % mod
        wh = (wh * base + ord(text[i])) % mod
    count = 0
    for i in range(n - m + 1):
        if wh == ph and text[i:i + m] == pattern:
            count += 1
        if i < n - m:
            wh = (wh - ord(text[i]) * high) % mod
            wh = (wh * base + ord(text[i + m])) % mod
    return count

print(count_occurrences("the fox met the fox by the fox hole", "fox"))  # 3

# This set matters because these are the workhorses behind real tools:
# inversion counts in ranking and collaborative filtering, all-pairs
# paths in transit planners, topological order in build systems,
# palindrome tricks in DNA analysis, and rolling-hash search in
# plagiarism detection.
