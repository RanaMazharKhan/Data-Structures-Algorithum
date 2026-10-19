# 0/1 knapsack and longest common subsequence (classic DP problems)

# 0/1 knapsack: n items, each with a weight and a value.
# A bag holds at most W weight. Take each item at most once (0 or 1).
# Recurrence: for each item, either skip it or take it (if it fits).
# knapsack(i, w) = max(knapsack(i-1, w), value[i] + knapsack(i-1, w - weight[i]))
def knapsack(values, weights, W):
    n = len(values)
    # dp[i][w] = best value using the first i items with capacity w
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] > w:
                dp[i][w] = dp[i - 1][w]  # item too heavy, skip it
            else:
                dp[i][w] = max(dp[i - 1][w],
                               values[i - 1] + dp[i - 1][w - weights[i - 1]])
    return dp[n][W]


# Example: laptop(2kg, $60), phone(1kg, $30), camera(3kg, $50), bag holds 4kg
values = [60, 30, 50]
weights = [2, 1, 3]
print(knapsack(values, weights, 4))  # 90 (laptop + phone = 3kg, $90)

# Longest common subsequence: the longest sequence that appears
# in both strings, keeping order but not necessarily together.
# Used in diff tools and spell checkers. lcs(i, j) compares the
# prefixes s1[:i] and s2[:j]: if the last chars match, add 1 and
# move both; otherwise take the better of dropping one char.
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


print(lcs("abcde", "ace"))     # 3 ("ace")
print(lcs("AGGTAB", "GXTXAYB"))  # 4 ("GTAB")

# These two are DP's most famous patterns: knapsack teaches the
# "take or skip" decision table, LCS teaches the "compare and shrink"
# table. Git diff, DNA alignment, and many packing/optimization
# problems in the real world run on exactly this logic.
