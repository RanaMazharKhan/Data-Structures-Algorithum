# A* search: shortest path with a good guess

# A* is Dijkstra with a hint. Each node gets a score f = g + h, where
# g is the real cost from the start and h is a guess of the cost left
# (here the Manhattan distance to the goal). A good guess that never
# overestimates makes A* reach the goal faster than plain Dijkstra.
import heapq

# 0 means free, 1 means a wall.
grid = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
start = (0, 0)
goal = (4, 4)


# The guess: Manhattan distance, the steps left if there were no walls.
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    # Heap entries are (f, g, position); the smallest f is explored first.
    heap = [(heuristic(start, goal), 0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    while heap:
        f, g, current = heapq.heappop(heap)
        if current == goal:
            break
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                new_cost = g + 1
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    heapq.heappush(heap, (new_cost + heuristic((nx, ny), goal),
                                          new_cost, (nx, ny)))
                    came_from[(nx, ny)] = current
    # Walk back from the goal to rebuild the path.
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    return list(reversed(path))


path = a_star(grid, start, goal)
print("path length:", len(path) - 1)  # steps from start to goal
print(path)

# Why it matters: A* is the classic pathfinder for games, maps and robots.
# The heuristic lets it aim straight at the goal instead of exploring
# in every direction, so it finds the shortest path much faster.
