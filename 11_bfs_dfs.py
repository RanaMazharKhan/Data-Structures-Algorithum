# BFS and DFS - two ways to walk through every node of a graph

# Build a small undirected graph as an adjacency list
# (same idea as 10_graph_basics.py)
graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

# BFS = breadth-first search. Visit nodes level by level, like ripples
# spreading out from a stone dropped in water. It uses a QUEUE:
# first-in first-out, so nearer nodes always get visited before
# farther ones.
def bfs(graph, start):
    visited = []
    queue = [start]      # queue starts with just the start node
    seen = {start}
    while queue:
        node = queue.pop(0)      # take the OLDEST waiting node
        visited.append(node)
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)   # new nodes go to the BACK
    return visited

print("BFS from A:", bfs(graph, "A"))
# BFS from A: ['A', 'B', 'C', 'D', 'E', 'F']
# A first, then its neighbors B, C, then their unvisited neighbors D, E, F


# DFS = depth-first search. Go as deep as possible down one path before
# trying the next. It uses a STACK (first-in last-out) or plain
# recursion - the call stack does the stacking for you.
def dfs(graph, start, seen=None):
    if seen is None:
        seen = set()
    seen.add(start)
    order = [start]
    for neighbor in graph[start]:
        if neighbor not in seen:
            order += dfs(graph, neighbor, seen)   # dive deep first
    return order

print("DFS from A:", dfs(graph, "A"))
# DFS from A: ['A', 'B', 'D', 'E', 'F', 'C']
# dives A -> B -> D, backtracks, then B -> E -> F, finally C


# Iterative DFS with an explicit stack (same result, no recursion)
def dfs_stack(graph, start):
    visited = []
    stack = [start]
    seen = {start}
    while stack:
        node = stack.pop()       # take the NEWEST waiting node
        visited.append(node)
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return visited

print("DFS (stack) from A:", dfs_stack(graph, "A"))


# Finding a path: BFS can also find the SHORTEST path (fewest hops)
# by remembering which node we came from.
def bfs_path(graph, start, goal):
    queue = [start]
    came_from = {start: None}
    while queue:
        node = queue.pop(0)
        if node == goal:
            break
        for neighbor in graph[node]:
            if neighbor not in came_from:
                came_from[neighbor] = node
                queue.append(neighbor)
    # walk backwards from the goal using the "came from" map
    if goal not in came_from:
        return None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    return path[::-1]

print("shortest path A -> F:", bfs_path(graph, "A", "F"))
# shortest path A -> F: ['A', 'C', 'F']


# BFS vs DFS cheat sheet:
# - BFS visits level by level (queue) -> finds the shortest path in
#   an unweighted graph. Used in: friend suggestions ("2 hops away"),
#   web crawlers, shortest path in a maze.
# - DFS dives deep first (stack/recursion) -> simpler code, less
#   memory. Used in: exploring every option (mazes, puzzles),
#   cycle detection, topological sort of task dependencies.

# Why it matters: almost every "connected to what?" question is BFS
# or DFS in disguise - routes, recommendations, reachability. Learn
# both, know when each shines.
