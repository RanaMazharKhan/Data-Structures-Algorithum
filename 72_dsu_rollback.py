# DSU with rollback: undo unions for offline queries

# Normal DSU uses path compression, which cannot be undone. For rollback
# we skip path compression and only use union by size, so every change
# is easy to reverse: we just remember what we changed.
class RollbackDSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.history = []

    # Find without path compression, so nothing changes during a find.
    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    # Union by size: attach the smaller tree under the bigger one.
    # Push the old values onto history so rollback can restore them.
    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            self.history.append(None)
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.history.append((b, self.parent[b], a, self.size[a]))
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

    # Remember the current history length, like a save point.
    def snapshot(self):
        return len(self.history)

    # Undo unions back to a snapshot, restoring parents and sizes.
    def rollback(self, snap):
        while len(self.history) > snap:
            change = self.history.pop()
            if change is None:
                continue
            b, old_parent, a, old_size = change
            self.parent[b] = old_parent
            self.size[a] = old_size


dsu = RollbackDSU(5)
dsu.union(0, 1)
dsu.union(2, 3)
print(dsu.connected(0, 1))  # True
print(dsu.connected(0, 2))  # False

# Save, try a temporary union, then undo it.
snap = dsu.snapshot()
dsu.union(1, 2)
print(dsu.connected(0, 3))  # True, while the temporary union holds
dsu.rollback(snap)
print(dsu.connected(0, 3))  # False again, the union is undone
print(dsu.connected(0, 1))  # True, the earlier union survives

# Why it matters: offline problems add edges, ask a question, then remove
# the edges again, like divide and conquer on queries. Rollback DSU lets
# you rewind safely instead of rebuilding the whole structure each time.
