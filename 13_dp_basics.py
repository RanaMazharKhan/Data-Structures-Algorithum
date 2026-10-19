# Dynamic programming: memoization vs tabulation, climbing stairs

# Plain recursion recomputes the same subproblems again and again.
# fib(5) calls fib(3) twice, fib(2) three times, and it blows up
# exponentially. Watch how slow it gets on larger inputs.
def fib_plain(n):
    if n <= 1:
        return n
    return fib_plain(n - 1) + fib_plain(n - 2)


print(fib_plain(10))  # 55

# Memoization: save each answer the first time we compute it, and
# reuse it later. Same code as plain recursion, plus a dict.
# This is top-down DP - we start at n and break it down.
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


print(fib_memo(35))  # 9227465, instantly - memo turns 2^n into n steps

# Tabulation: build a table bottom-up instead of recursing.
# Solve fib(0), fib(1), ..., fib(n) in order, each from the
# previous two. No recursion, no dict, uses a simple list.
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


print(fib_tab(35))  # 9227465

# Climbing stairs: you can take 1 or 2 steps at a time.
# How many ways to reach step n? Ways(n) = Ways(n-1) + Ways(n-2)
# because your last step was either 1 step (from n-1) or 2 steps (from n-2).
# It is the same shape as fibonacci, which is the point of DP:
# recognize the overlapping subproblems and cache them.
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2  # ways for step 1 and step 2
    for _ in range(3, n + 1):
        a, b = b, a + b  # only keep the last two values
    return b


print(climb_stairs(5))   # 8 ways
print(climb_stairs(10))  # 89 ways

# DP matters because a huge class of interview problems - knapsack,
# edit distance, coin change, longest common subsequence - are all
# "overlapping subproblems + cache the answer" in disguise.
# Learn this pattern once and you can unlock all of them.
