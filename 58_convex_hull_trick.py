# Convex hull trick: speeding up DP with lines

# Many DP problems end up asking: given a set of lines y = m*x + b,
# what is the smallest value at x? Checking every line is O(n) per query.
# If lines are added with decreasing slopes and queries come with
# increasing x, a deque keeps only the lines that can ever win, so each
# query is O(1) amortised.
class Line:
    def __init__(self, m, b):
        self.m = m
        self.b = b

    def value(self, x):
        return self.m * x + self.b


# Line l2 is useless if it is never below both l1 and l3.
# We compare intersection points without floating point numbers:
# (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3) means l2 can go.
def is_bad(l1, l2, l3):
    return (l3.b - l1.b) * (l1.m - l2.m) <= (l2.b - l1.b) * (l1.m - l3.m)


class ConvexHullTrick:
    def __init__(self):
        self.lines = []

    # Add a line; slopes must arrive in decreasing order.
    def add_line(self, m, b):
        new = Line(m, b)
        while len(self.lines) >= 2 and is_bad(self.lines[-2], self.lines[-1], new):
            self.lines.pop()
        self.lines.append(new)

    # Query the minimum at x; x values must arrive in increasing order.
    def query(self, x):
        while len(self.lines) >= 2 and self.lines[0].value(x) >= self.lines[1].value(x):
            self.lines.pop(0)
        return self.lines[0].value(x)


# Example: lines y = 2x + 1, y = -x + 10, y = x + 3 is not in
# decreasing-slope order, so we add them sorted: slopes 2, 1, -1.
cht = ConvexHullTrick()
cht.add_line(2, 1)
cht.add_line(1, 3)
cht.add_line(-1, 10)
for x in [0, 1, 2, 3, 4]:
    print(x, cht.query(x))

# Check against brute force: at each x, take the min over all lines.
lines = [(2, 1), (1, 3), (-1, 10)]
for x in [0, 2, 4]:
    brute = min(m * x + b for m, b in lines)
    print("brute at", x, "=", brute)

# A classic DP use: dp[i] = min over j of dp[j] + (x[i] - x[j])^2
# expands to lines with slope -2*x[j] and intercept dp[j] + x[j]^2,
# queried at x[i]. That turns an O(n^2) DP into O(n).
xs = [0, 1, 2, 3]
dp = [0] * len(xs)
cht2 = ConvexHullTrick()
cht2.add_line(0, 0)  # j = 0: slope -2*0, intercept dp[0] + 0
for i in range(1, len(xs)):
    dp[i] = cht2.query(xs[i]) + xs[i] * xs[i]
    cht2.add_line(-2 * xs[i], dp[i] + xs[i] * xs[i])
print(dp)  # [0, 1, 2, 3]: cheapest steps move one position at a time

# Why it matters: it turns quadratic DP problems into linear ones.
# It shows up in partitioning, batch scheduling and DP optimisation tasks.
