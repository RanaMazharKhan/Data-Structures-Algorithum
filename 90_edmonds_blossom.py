# Edmonds' blossom algorithm: maximum matching in general graphs

# A matching pairs up vertices so no vertex is used twice, and the
# maximum matching uses as many pairs as possible. On bipartite
# graphs Hopcroft-Karp does this, but on general graphs odd cycles
# break it: an augmenting path can enter an odd cycle (a "blossom")
# and a plain BFS cannot tell which way around the cycle to go.
# Edmonds' fix is to shrink the whole blossom into one super-node,
# find the path in the shrunk graph, then lift it back out again.
from collections import deque

def max_matching(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    match = [-1] * n
    base = list(range(n))
    parent = [-1] * n
    used = [False] * n
    blossom = [False] * n

    # lowest common ancestor of two vertices in the BFS tree,
    # walking up through matched edges only
    def lca(a, b):
        seen = [False] * n
        while True:
            a = base[a]
            seen[a] = True
            if match[a] == -1:
                break
            a = parent[match[a]]
        while True:
            b = base[b]
            if seen[b]:
                return b
            b = parent[match[b]]

    # mark every vertex of the blossom found between v and the
    # base b, remembering which way around the cycle to walk back
    def mark_path(v, b, child):
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            parent[v] = child
            child = match[v]
            v = parent[match[v]]

    # BFS from a free vertex looking for another free vertex;
    # blossoms found on the way are shrunk into their base
    def find_path(root):
        nonlocal parent, base, used, blossom
        used = [False] * n
        parent = [-1] * n
        base = list(range(n))
        queue = deque([root])
        used[root] = True
        while queue:
            v = queue.popleft()
            for to in graph[v]:
                if base[v] == base[to] or match[v] == to:
                    continue
                if to == root or (match[to] != -1 and parent[match[to]] != -1):
                    cur = lca(v, to)
                    blossom = [False] * n
                    mark_path(v, cur, to)
                    mark_path(to, cur, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True
                                queue.append(i)
                elif parent[to] == -1:
                    parent[to] = v
                    if match[to] == -1:
                        # augmenting path found: flip every edge
                        # along it, matching grows by one pair
                        cur = to
                        while cur != -1:
                            prev = parent[cur]
                            nxt = match[prev] if prev != -1 else -1
                            match[cur] = prev
                            if prev != -1:
                                match[prev] = cur
                            cur = nxt
                        return True
                    else:
                        nxt = match[to]
                        used[nxt] = True
                        queue.append(nxt)
        return False

    for v in range(n):
        if match[v] == -1:
            find_path(v)
    return match

def pairs(match):
    return [(u, v) for u, v in enumerate(match) if v != -1 and u < v]

# two triangles sharing one vertex: a plain BFS gets stuck in the
# odd cycle, but shrinking the blossom finds the perfect matching
edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 2)]
match = max_matching(6, edges)
print(pairs(match))  # [(0, 1), (2, 3), (4, 5)] - all 6 vertices paired

# a triangle with a tail: only two pairs are possible
edges2 = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]
match2 = max_matching(5, edges2)
print(pairs(match2))  # [(0, 1), (2, 3)] - vertex 4 stays unmatched

# Edmonds' blossom matters wherever pairing has no "two sides":
# assigning roommates, pairing players for a tournament round,
# kidney-exchange chains, and any maximum matching on a general graph.
