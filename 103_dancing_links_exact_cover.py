# Dancing Links (Algorithm X): exact cover and Sudoku solving

# An exact cover problem: given rows that each cover some
# columns, pick rows so every column is covered exactly once.
# Dancing Links stores the matrix as a web of doubly linked
# nodes. Covering a column unlinks it and every row touching
# it; uncovering restores them in reverse, so backtracking is
# just relinking pointers. Algorithm X always picks the column
# with the fewest rows left, which prunes the search hard.

class Node:
    def __init__(self, col=None):
        self.left = self.right = self.up = self.down = self
        self.col = col
        self.row = -1

class Column(Node):
    def __init__(self, name):
        super().__init__(self)
        self.name = name
        self.size = 0

class DLX:
    def __init__(self, num_cols):
        self.header = Column("header")
        self.cols = []
        prev = self.header
        for i in range(num_cols):
            col = Column(i)
            col.left = prev
            col.right = self.header
            prev.right = col
            self.header.left = col
            prev = col
            self.cols.append(col)
        self.solution = []

    def add_row(self, row_id, col_ids):
        first = None
        for cid in col_ids:
            col = self.cols[cid]
            node = Node(col)
            node.row = row_id
            # link vertically into the column
            node.up = col.up
            node.down = col
            col.up.down = node
            col.up = node
            col.size += 1
            # link horizontally into the row
            if first is None:
                first = node
            else:
                node.left = first.left
                node.right = first
                first.left.right = node
                first.left = node

    def cover(self, col):
        col.right.left = col.left
        col.left.right = col.right
        row = col.down
        while row is not col:
            node = row.right
            while node is not row:
                node.down.up = node.up
                node.up.down = node.down
                node.col.size -= 1
                node = node.right
            row = row.down

    def uncover(self, col):
        row = col.up
        while row is not col:
            node = row.left
            while node is not row:
                node.col.size += 1
                node.down.up = node
                node.up.down = node
                node = node.left
            row = row.up
        col.right.left = col
        col.left.right = col

    def search(self):
        if self.header.right is self.header:
            return True
        # pick the column with the fewest rows left
        col = self.header.right
        best = col
        while col is not self.header:
            if col.size < best.size:
                best = col
            col = col.right
        col = best
        if col.size == 0:
            return False
        self.cover(col)
        row = col.down
        while row is not col:
            self.solution.append(row.row)
            node = row.right
            while node is not row:
                self.cover(node.col)
                node = node.right
            if self.search():
                return True
            self.solution.pop()
            node = row.left
            while node is not row:
                self.uncover(node.col)
                node = node.left
            row = row.down
        self.uncover(col)
        return False

# Example: cover {1, 2, 3, 4, 5, 6} using the sets below.
sets = {
    "A": [0, 1, 2],
    "B": [1, 3],
    "C": [2, 4],
    "D": [3, 4, 5],
    "E": [0, 5],
}
names = list(sets)
dlx = DLX(6)
for i, name in enumerate(names):
    dlx.add_row(i, sets[name])
print("exact cover found:", dlx.search())
print("rows used:", [names[i] for i in dlx.solution])

# Sudoku as exact cover: each placed digit must satisfy four
# rules, one column per rule: the cell is filled, the row has
# the digit, the column has the digit, the box has the digit.
# A 4x4 board has 64 columns and 64 possible placements.
def solve_sudoku_4x4(puzzle):
    n = 4
    dlx = DLX(4 * n * n)
    placements = []  # (row, col, digit) for each added row
    for r in range(n):
        for c in range(n):
            for d in range(n):
                if puzzle[r][c] != 0 and puzzle[r][c] != d + 1:
                    continue
                box = (r // 2) * 2 + (c // 2)
                cols = [r * n + c,
                        n * n + r * n + d,
                        2 * n * n + c * n + d,
                        3 * n * n + box * n + d]
                dlx.add_row(len(placements), cols)
                placements.append((r, c, d + 1))
    if not dlx.search():
        return None
    board = [[0] * n for _ in range(n)]
    for i in dlx.solution:
        r, c, d = placements[i]
        board[r][c] = d
    return board

puzzle = [
    [1, 0, 3, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 3],
    [0, 0, 2, 0],
]
print("4x4 Sudoku solution:")
for row in solve_sudoku_4x4(puzzle):
    print(row)

# Dancing Links matters because exact cover hides inside many
# real problems: Sudoku, pentomino tiling, N-queens and
# scheduling, all solved by the same tiny pointer dance.
