# Min-cost max flow: send as much flow as possible at the lowest total cost

# Max flow only cares about amount. Min-cost max flow also cares about price:
# every edge has a capacity AND a cost per unit of flow. We want the maximum
# flow, and among all max flows, the cheapest one. Think of shipping goods:
# each road has a truck limit (capacity) and a price per truck (cost).
# Idea: keep finding the cheapest path from source to sink that still has
# room (using Bellman-Ford, because reverse edges can have negative cost),
# push as much flow as that path allows, and repeat until no path is left.
# A reverse edge with negative cost lets the algorithm "undo" an earlier
# choice if a cheaper route appears later - that is the key trick.
class MinCostMaxFlow:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]  # each edge: [to, capacity, cost, rev_index]

    def add_edge(self, u, v, capacity, cost):
        self.graph[u].append([v, capacity, cost, len(self.graph[v])])
        self.graph[v].append([u, 0, -cost, len(self.graph[u]) - 1])

    def flow(self, source, sink):
        total_flow = 0
        total_cost = 0
        INF = float("inf")
        while True:
            # Bellman-Ford: shortest (cheapest) path in terms of cost
            dist = [INF] * self.n
            prev_node = [-1] * self.n
            prev_edge = [-1] * self.n
            dist[source] = 0
            for _ in range(self.n - 1):
                updated = False
                for u in range(self.n):
                    if dist[u] == INF:
                        continue
                    for i, (v, cap, cost, _) in enumerate(self.graph[u]):
                        if cap > 0 and dist[v] > dist[u] + cost:
                            dist[v] = dist[u] + cost
                            prev_node[v] = u
                            prev_edge[v] = i
                            updated = True
                if not updated:
                    break
            if dist[sink] == INF:  # no more room from source to sink
                break
            # How much flow can this cheapest path carry?
            push = INF
            v = sink
            while v != source:
                u = prev_node[v]
                push = min(push, self.graph[u][prev_edge[v]][1])
                v = u
            # Push it and update reverse edges
            v = sink
            while v != source:
                u = prev_node[v]
                i = prev_edge[v]
                edge = self.graph[u][i]
                edge[1] -= push
                self.graph[v][edge[3]][1] += push
                total_cost += push * edge[2]
                v = u
            total_flow += push
        return total_flow, total_cost


# Example: warehouse (0) ships to shop (3) through two routes
# 0 -> 1 costs 1 per unit, capacity 4; 0 -> 2 costs 2 per unit, capacity 3
# 1 -> 3 costs 2 per unit, capacity 4; 2 -> 3 costs 1 per unit, capacity 3
# plus a cheap cross road 1 -> 2 costing 1, capacity 2
mcmf = MinCostMaxFlow(4)
mcmf.add_edge(0, 1, 4, 1)
mcmf.add_edge(0, 2, 3, 2)
mcmf.add_edge(1, 3, 4, 2)
mcmf.add_edge(2, 3, 3, 1)
mcmf.add_edge(1, 2, 2, 1)
flow, cost = mcmf.flow(0, 3)
print("max flow:", flow)        # 7 (all trucks get through)
print("min total cost:", cost)  # cheapest way to send those 7 units

# Why it matters: min-cost flow models real logistics - shipping goods,
# assigning workers to jobs, or routing data - where every unit has a price
# and you want the most delivered for the least money.
