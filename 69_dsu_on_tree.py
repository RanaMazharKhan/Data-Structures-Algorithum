# DSU on tree: small-to-large answers on subtrees

# Small-to-large means: when merging two sets, always pour the
# smaller one into the bigger one. Each element then moves only
# O(log n) times, so merging whole subtrees stays fast.
# Here we count the distinct colours in every subtree of a tree.

# Tree as adjacency list, rooted at 0. colours[i] is node i's colour.
tree = {0: [1, 2], 1: [3, 4], 2: [5], 3: [], 4: [], 5: []}
colours = ["red", "blue", "red", "green", "blue", "red"]
answer = {}


# Returns the set of colours in this subtree, reusing the biggest
# child's set so we copy as little as possible.
def dfs(node):
    biggest = set()
    for child in tree[node]:
        child_set = dfs(child)
        if len(child_set) > len(biggest):
            biggest, child_set = child_set, biggest
        biggest.update(child_set)
    biggest.add(colours[node])
    answer[node] = len(biggest)
    return biggest


dfs(0)
print(answer)  # node 0 sees 3 colours, node 1 sees 2, leaves see 1
print("distinct colours in whole tree:", answer[0])  # 3
print("distinct colours under node 1:", answer[1])   # 2 (blue, green)

# Why it matters: questions like "how many distinct values are in this
# subtree?" appear in coding contests and interviews. Small-to-large
# turns a slow merge-everything solution into one that easily passes.
