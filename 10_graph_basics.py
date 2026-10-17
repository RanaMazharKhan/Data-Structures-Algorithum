# Graph basics - represent graphs with an adjacency list, add edges, print them

# Idea: a graph is just nodes connected by edges. The simplest way to store
# one is a dict: each node maps to the list of its neighbors. This is the
# "adjacency list", fast and easy to build.
class Graph:
    def __init__(self):
        self.nodes = {}   # node -> list of neighbors

    # add an edge between two nodes (undirected: both directions)
    def add_edge(self, a, b):
        if a not in self.nodes:
            self.nodes[a] = []
        if b not in self.nodes:
            self.nodes[b] = []
        self.nodes[a].append(b)
        self.nodes[b].append(a)

    def neighbors(self, node):
        return self.nodes.get(node, [])

    def print_graph(self):
        for node in self.nodes:
            print(node, "->", self.nodes[node])

g = Graph()
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.add_edge("C", "D")

g.print_graph()
# A -> ['B', 'C']
# B -> ['A', 'D']
# C -> ['A', 'D']
# D -> ['B', 'C']

print(g.neighbors("A"))   # ['B', 'C']


# Directed graph: an edge only goes one way (like a one-way street, or
# "user A follows user B" on social media). Just skip the reverse link.
class DirectedGraph:
    def __init__(self):
        self.nodes = {}

    def add_edge(self, a, b):   # a -> b only
        if a not in self.nodes:
            self.nodes[a] = []
        if b not in self.nodes:
            self.nodes[b] = []
        self.nodes[a].append(b)

    def print_graph(self):
        for node in self.nodes:
            print(node, "->", self.nodes[node])

d = DirectedGraph()
d.add_edge("you", "teacher")
d.add_edge("you", "mentor")
d.add_edge("teacher", "mentor")
d.print_graph()
# you -> ['teacher', 'mentor']
# teacher -> ['mentor']
# mentor -> []

print("neighbors of teacher:", d.nodes["teacher"])   # ['mentor']


# Why it matters: graphs are everywhere - road maps, friend networks,
# the web, dependency chains. Almost every "paths and connections"
# problem (shortest route, social suggestions) starts by building one
# of these, so getting comfortable with the adjacency list pays off.
