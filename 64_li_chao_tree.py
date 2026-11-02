# Li Chao tree - answer "lowest line at x" queries fast
# We have many lines y = m*x + b, and queries ask for the
# minimum value at some x. No need for slopes to be sorted.
# Each tree node stores the line that is best at the middle x.

class Line:
    def __init__(self, m, b):
        self.m = m
        self.b = b

    def value(self, x):
        return self.m * x + self.b


class LiChaoTree:
    def __init__(self, x_min, x_max):
        self.x_min = x_min
        self.x_max = x_max
        self.line = None
        self.left = None
        self.right = None

    # insert a new line into this range
    def insert(self, new_line):
        self._insert(new_line, self.x_min, self.x_max)

    def _insert(self, new_line, lo, hi):
        mid = (lo + hi) // 2
        if self.line is None:
            self.line = new_line
            return

        # at mid, keep the better line here, push the worse one down
        if new_line.value(mid) < self.line.value(mid):
            self.line, new_line = new_line, self.line

        if lo == hi:
            return

        # the losing line can only win on one side of mid
        if new_line.value(lo) < self.line.value(lo):
            if self.left is None:
                self.left = LiChaoTree(lo, mid)
            self.left._insert(new_line, lo, mid)
        elif new_line.value(hi) < self.line.value(hi):
            if self.right is None:
                self.right = LiChaoTree(mid + 1, hi)
            self.right._insert(new_line, mid + 1, hi)

    # query the minimum value at x
    def query(self, x):
        return self._query(x, self.x_min, self.x_max)

    def _query(self, x, lo, hi):
        best = self.line.value(x) if self.line else float("inf")
        if lo == hi:
            return best
        mid = (lo + hi) // 2
        if x <= mid and self.left:
            best = min(best, self.left._query(x, lo, mid))
        if x > mid and self.right:
            best = min(best, self.right._query(x, mid + 1, hi))
        return best


# Example: lines y = x, y = -x + 10, y = 2x - 4
tree = LiChaoTree(x_min=-10, x_max=10)
tree.insert(Line(1, 0))
tree.insert(Line(-1, 10))
tree.insert(Line(2, -4))

for x in [-5, 0, 3, 8]:
    print("x =", x, "-> min =", tree.query(x))

# ---
# Why it matters: Li Chao trees power DP optimization problems
# (like "divide and conquer DP" or "convex hull trick without
# sorted slopes") and any problem where many lines compete
# and you need the best value at many x positions.
