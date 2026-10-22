# Rabin-Karp: string matching with rolling hashes

# The idea: instead of comparing the pattern against every window
# character by character, hash each window. Slide the window one step
# by removing the leftmost character's contribution and adding the new
# rightmost one - O(1) per step. Compare characters only when the hashes
# match (kills false positives from hash collisions). O(n + m) average.
def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n or m == 0:
        return []

    base, mod = 256, 10**9 + 7
    high = pow(base, m - 1, mod)  # base^(m-1), weight of first char

    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    matches = []
    for i in range(n - m + 1):
        if window_hash == pattern_hash and text[i:i + m] == pattern:
            matches.append(i)
        if i < n - m:
            # roll the window: drop text[i], add text[i + m]
            window_hash = (window_hash - ord(text[i]) * high) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
    return matches


# Demo: find every occurrence of "ab" in a long string.
print(rabin_karp("ababcababcab", "ab"))   # [0, 2, 5, 7, 10]

# Demo: a classic multiple-pattern use case - plagiarism scanning:
# check which of several phrases appear in a document.
document = "the quick brown fox jumps over the lazy dog"
for phrase in ["quick brown", "lazy cat", "over the"]:
    print(phrase, "->", rabin_karp(document, phrase))

# Why it matters: the classic fast way to search for many patterns at
# once (hash all patterns, scan the text once) - used in plagiarism
# detectors, grep-style tools, and DNA sequence searching.
