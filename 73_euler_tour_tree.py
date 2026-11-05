# Euler tour tree: subtree queries as range queries

# A tree is hard to query by subtree, but a flat list is easy. An Euler
# tour walks the tree in DFS order and gives every node an entry time.
# All nodes of a subtree then sit together in one continuous range.
tree = {
    0: [1, 2],
    1: [3, 4],
    2: [5],
    3: [],
    4: [],
    5: [],
}
value = {0: 10, 1: 20, 2: 30, 3: 40, 4: 50, 5: 60}

tin = {}
tout = {}
flat = []
timer = 0

# DFS: record entry time, visit children, then record exit time.
# The subtree of a node is exactly flat[tin[node] .. tout[node]].
def dfs(node):
    global timer
    tin[node] = timer
    flat.append(value[node])
    timer += 1
    for child in tree[node]:
        dfs(child)
    tout[node] = timer - 1


dfs(0)
print(flat)  # [10, 20, 40, 50, 30, 60], DFS order

# Prefix sums turn any range sum into one subtraction.
prefix = [0]
for x in flat:
    prefix.append(prefix[-1] + x)

def subtree_sum(node):
    return prefix[tout[node] + 1] - prefix[tin[node]]

print(subtree_sum(0))  # 210, the whole tree
print(subtree_sum(1))  # 110, nodes 1, 3 and 4
print(subtree_sum(2))  # 90, nodes 2 and 5
print(subtree_sum(3))  # 40, just node 3

# Why it matters: subtree sums, counts and similar questions become
# simple range queries, which a Fenwick tree or segment tree can also
# answer with updates. It is used in file systems, org charts and
# any tree where you often ask about a whole subtree at once.
