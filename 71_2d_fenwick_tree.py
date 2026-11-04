# 2D Fenwick tree: rectangle sums on a grid

# A 1D Fenwick tree answers prefix sums fast. The 2D version does the
# same on a grid: it stores partial sums so any rectangle sum is a
# few prefix sums, and updating one cell is just as fast.
# Rows and columns are 1-based inside the tree, like the 1D version.
class Fenwick2D:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]

    # Add delta to cell (r, c). Walks up using lowbit, same as 1D,
    # but in both directions at once.
    def add(self, r, c, delta):
        i = r
        while i <= self.rows:
            j = c
            while j <= self.cols:
                self.tree[i][j] += delta
                j += j & -j
            i += i & -i

    # Sum of the rectangle from (1, 1) to (r, c).
    def prefix_sum(self, r, c):
        total = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                total += self.tree[i][j]
                j -= j & -j
            i -= i & -i
        return total

    # Sum of rows r1..r2 and columns c1..c2, using inclusion-exclusion:
    # whole block minus the strips above and left, plus the corner twice removed.
    def range_sum(self, r1, c1, r2, c2):
        return (self.prefix_sum(r2, c2)
                - self.prefix_sum(r1 - 1, c2)
                - self.prefix_sum(r2, c1 - 1)
                + self.prefix_sum(r1 - 1, c1 - 1))


# A small 3x3 grid, filled cell by cell.
grid = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
bit = Fenwick2D(3, 3)
for r in range(3):
    for c in range(3):
        bit.add(r + 1, c + 1, grid[r][c])

print(bit.prefix_sum(2, 2))        # 12, the top-left 2x2 block
print(bit.range_sum(2, 2, 3, 3))   # 28, the bottom-right 2x2 block
print(bit.range_sum(1, 1, 3, 3))   # 45, the whole grid

# Update one cell: cell (2, 2) goes from 5 to 15, so add 10.
bit.add(2, 2, 10)
print(bit.range_sum(2, 2, 3, 3))   # 38, updated without rebuilding
print(bit.range_sum(1, 1, 3, 3))   # 55, the new whole-grid total

# Why it matters: spreadsheets, images and game maps all need "sum of
# this rectangle" queries with frequent point updates. A 2D Fenwick
# tree answers both in logarithmic time instead of scanning the grid.
