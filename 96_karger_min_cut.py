# Karger's algorithm: randomized global minimum cut by edge contraction

# The global min cut is the smallest set of edges whose removal
# splits the graph into two parts. Karger's idea: pick a random
# edge, contract it (merge its two endpoints into one vertex,
# keeping all other edges), and repeat until only 2 vertices
# remain. The edges left between them are a cut. One run can
# miss the true min cut, but repeating it many times makes the
# chance of missing it tiny. Simple and fast: O(n^2) per run.

import random

# Contract one random edge: merge v into u, drop self-loops.
# Vertices are kept as lists of original labels so we can see
# which original vertices ended up on each side of the cut.
def contract(graph):
    # graph: dict vertex -> list of neighbours (parallel edges kept
    # as repeated entries, they matter for the cut size)
    vertices = {v: [v] for v in graph}
    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.append((u, v))
    while len(vertices) > 2:
        u, v = random.choice(edges)
        # merge v into u
        vertices[u] = vertices[u] + vertices[v]
        del vertices[v]
        new_edges = []
        for a, b in edges:
            if a == v:
                a = u
            if b == v:
                b = u
            if a != b:  # self-loop, discard it
                new_edges.append((a, b))
        edges = new_edges
    # the remaining edges are exactly the cut
    side_a = list(vertices.values())[0]
    return len(edges), side_a

# Run the contraction many times and keep the smallest cut found.
def karger_min_cut(graph, trials=200):
    best = None
    best_side = None
    for _ in range(trials):
        size, side = contract(graph)
        if best is None or size < best:
            best, best_side = size, side
    return best, best_side

# a small graph: two triangles joined by two links, so the true
# min cut is 2 (cut both links, or cut one triangle's edges)
graph = {
    0: [1, 2, 3],
    1: [0, 2],
    2: [0, 1, 3],
    3: [0, 2, 4, 5],
    4: [3, 5],
    5: [3, 4],
}
random.seed(42)
size, side = karger_min_cut(graph, trials=200)
print("min cut size:", size)
print("one side of the cut:", sorted(side))

# Karger's algorithm matters because the global min cut shows the
# weakest point of a network: the fewest links whose failure
# splits it in two. It is used in network reliability, community
# detection, and as a fast building block inside other algorithms.
