# Backtracking: try choices one by one, undo a choice when it fails, keep going

# Backtracking explores a solution step by step. At each step you make
# a choice, check if it is still possible, and if you hit a dead end
# you UNDO the choice ("backtrack") and try the next option. It is how
# you brute-force problems with constraints: puzzles, subsets, combos.

# N-Queens: place n queens on an n x n board so no two attack each
# other. Try each row for the queen of the current column; if a row is
# attacked, skip it; if no row works, backtrack to the previous column.
def n_queens(n):
    solutions = []
    queens = [-1] * n  # queens[col] = row of the queen in that column

    # safe if no earlier queen shares this row or a diagonal
    def safe(col, row):
        for c in range(col):
            if queens[c] == row or abs(queens[c] - row) == abs(c - col):
                return False
        return True

    def place(col):
        if col == n:            # all columns filled -> found a solution
            solutions.append(queens[:])
            return
        for row in range(n):    # try every row in this column
            if safe(col, row):
                queens[col] = row
                place(col + 1)  # go deeper with this choice
                queens[col] = -1  # undo the choice (backtrack)

    place(0)
    return solutions

sols = n_queens(4)
print("4-queens solutions:", len(sols))  # 2
for s in sols:
    print(" ".join(str(r + 1) for r in s))  # rows 1-4, one per column

# Subset generation: for each element, choose INCLUDE or EXCLUDE.
# That is 2 choices per element, so all subsets = 2^n of them.
def subsets(nums):
    result = []
    def build(i, current):
        if i == len(nums):          # past the last element -> save subset
            result.append(current[:])
            return
        current.append(nums[i])     # choice 1: include nums[i]
        build(i + 1, current)
        current.pop()               # undo (backtrack)
        build(i + 1, current)       # choice 2: exclude nums[i]
    build(0, [])
    return result

print(subsets([1, 2, 3]))
# [[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]] - all 8 subsets

# Backtracking matters because it is the engine behind Sudoku solvers,
# crossword fillers, password/permutation generators, and maze solving.
# The pattern is always the same: choose -> check -> recurse -> undo.
