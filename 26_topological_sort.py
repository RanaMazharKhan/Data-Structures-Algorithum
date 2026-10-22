# Topological sort: ordering tasks with dependencies (Kahn's algorithm)

# The idea (Kahn): count each node's incoming edges. Start with the
# nodes that have zero incoming edges (nothing depends before them).
# Remove one, "delete" its outgoing edges (decrease indegree of its
# neighbours), and repeat. O(nodes + edges). Only works on DAGs -
# a cycle means some tasks block each other forever, so the result
# is shorter than the node count when a cycle exists.
from collections import deque

def topological_sort(nodes, edges):
    graph = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for u, v in edges:        # u must come before v
        graph[u].append(v)
        indegree[v] += 1

    queue = deque([n for n in nodes if indegree[n] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            indegree[neighbour] -= 1
            if indegree[neighbour] == 0:
                queue.append(neighbour)

    if len(order) != len(nodes):
        return None  # cycle detected - no valid ordering exists
    return order


# Demo: get dressed. Socks before shoes, shirt before jacket, etc.
tasks = ['shirt', 'jacket', 'socks', 'shoes', 'pants', 'belt']
deps = [
    ('shirt', 'jacket'),  # jacket goes on after the shirt
    ('socks', 'shoes'),   # shoes go on after socks
    ('pants', 'belt'),    # belt goes on after pants
    ('pants', 'shoes'),   # shoes go on after pants
]
print(topological_sort(tasks, deps))
# any valid order, e.g. shirt, socks, pants, jacket, belt, shoes

# Demo: a cycle is caught - A needs B and B needs A is impossible.
print(topological_sort(['A', 'B'], [('A', 'B'), ('B', 'A')]))  # None

# Why it matters: build systems and package managers (pip, npm) install
# dependencies in topological order, course schedulers order
# prerequisites, and spreadsheets recalculate cells this way.
