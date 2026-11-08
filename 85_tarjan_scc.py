# Tarjan's algorithm: strongly connected components in one DFS

# In a directed graph, a strongly connected component (SCC) is a group
# of nodes where every node can reach every other node in the group.
# Tarjan's idea: run one DFS and number each node by the order it is
# first seen. Track the lowest number reachable from each node through
# its descendants (the lowlink). When a node's number equals its
# lowlink, it is the root of an SCC, and every node above it on the
# DFS stack belongs to that same component.
import sys
sys.setrecursionlimit(10000)

def tarjan(n, graph):
    index = [0] * n        # discovery order, 0 means unvisited
    lowlink = [0] * n      # lowest index reachable from this node
    on_stack = [False] * n
    stack = []
    result = []
    counter = [0]

    def dfs(u):
        counter[0] += 1
        index[u] = lowlink[u] = counter[0]
        stack.append(u)
        on_stack[u] = True
        for v in graph[u]:
            if index[v] == 0:
                dfs(v)
                lowlink[u] = min(lowlink[u], lowlink[v])
            elif on_stack[v]:
                lowlink[u] = min(lowlink[u], index[v])
        # u is the root of an SCC when no descendant reaches earlier
        if lowlink[u] == index[u]:
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == u:
                    break
            result.append(component)

    for i in range(n):
        if index[i] == 0:
            dfs(i)
    return result

# 0 -> 1 -> 2 -> 0 forms a cycle, 3 -> 4 is one-way, 2 points to 3
graph = [[1], [2], [0, 3], [4], []]
sccs = tarjan(5, graph)
print(sccs)  # [[4], [3], [2, 1, 0]] - 0, 1 and 2 reach each other

# a lone node with no cycle back to itself is its own component,
# which is why 3 and 4 each appear alone even though 3 points to 4
print(len(sccs))  # 3 components in this graph

# Tarjan's matters wherever direction and cycles matter: finding
# groups of web pages that link to each other, spotting circular
# dependencies in code, and solving 2-SAT - one DFS finds them all.
