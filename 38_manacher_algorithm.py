# Manacher's algorithm: longest palindromic substring in O(n)

# A palindrome reads the same forwards and backwards, like "racecar".
# The naive way checks every centre and expands outwards, which is O(n^2).
# Manacher's trick: remember the palindrome that reaches furthest right,
# and mirror the answer for centres inside it instead of re-expanding.

def longest_palindrome(s):
    # put # between characters so odd and even palindromes look the same
    # "aba" becomes "^#a#b#a#$" (^ and $ are guards, never matched)
    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    p = [0] * n  # p[i] = radius of the palindrome centred at i
    centre = right = 0
    for i in range(1, n - 1):
        mirror = 2 * centre - i
        if i < right:
            # i is inside a known palindrome, mirror its radius
            p[i] = min(right - i, p[mirror])
        # try to expand around i
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > right:
            centre, right = i, i + p[i]
    # the biggest radius gives the longest palindrome
    best = max(range(n), key=lambda i: p[i])
    start = (best - p[best]) // 2
    return s[start:start + p[best]]


print(longest_palindrome("babad"))   # "bab" (or "aba", both length 3)
print(longest_palindrome("cbbd"))    # "bb"
print(longest_palindrome("racecar"))  # "racecar"
print(longest_palindrome("abc"))     # "a"

# ---
# Why it matters: Manacher's algorithm finds the longest palindrome in
# linear time, so it is used in DNA analysis, text processing and
# interview problems where the O(n^2) expansion is too slow.
