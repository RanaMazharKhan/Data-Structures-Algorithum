# Suffix arrays: sort every suffix of a string once, search fast forever
# The suffix array of "banana" is [5, 3, 1, 0, 4, 2] because the suffixes
# sorted are: "a", "ana", "anana", "banana", "na", "nana". Once sorted,
# finding any substring is a binary search over the suffixes, and the
# LCP (longest common prefix) of neighbours reveals repeated substrings.

def build_suffix_array(s):
    # simple O(n^2 log n) version: sort the suffix start indexes
    return sorted(range(len(s)), key=lambda i: s[i:])


# binary search the suffix array for a pattern's first occurrence
def substring_search(s, sa, pattern):
    lo, hi = 0, len(sa)
    while lo < hi:
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid] + len(pattern)] < pattern:
            lo = mid + 1
        else:
            hi = mid
    if lo < len(sa) and s.startswith(pattern, sa[lo]):
        return sa[lo]
    return -1


# longest repeated substring = max LCP between adjacent suffixes
def longest_repeated(s, sa):
    best, pos = 0, -1
    for a, b in zip(sa, sa[1:]):
        lcp = 0
        while a + lcp < len(s) and b + lcp < len(s) and s[a + lcp] == s[b + lcp]:
            lcp += 1
        if lcp > best:
            best, pos = lcp, a
    return s[pos:pos + best]


# Example
text = "banana"
sa = build_suffix_array(text)
print(sa)                              # [5, 3, 1, 0, 4, 2]
print(substring_search(text, sa, "ana"))  # 3 (suffix "ana" starts at index 3)
print(substring_search(text, sa, "xyz"))  # -1 (not present)
print(longest_repeated(text, sa))       # 'ana'

# ---
# Why it matters: suffix arrays (and their bigger cousin, suffix trees)
# are how text search engines, DNA analysis tools and diff algorithms
# find repeats and matches in huge strings after a single preprocessing.
