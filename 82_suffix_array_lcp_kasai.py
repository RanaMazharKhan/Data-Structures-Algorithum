# Suffix array + LCP with Kasai: sort all suffixes, then measure shared prefixes

# A suffix array lists the starting positions of all suffixes of a
# string in sorted order. The doubling method sorts by the first 1,
# then 2, then 4, then 8 characters - each round reuses the previous
# ranks, so the whole sort takes O(n log n).
def suffix_array(s):
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n
    k = 1
    while k < n:
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, cur = sa[i - 1], sa[i]
            prev_key = (rank[prev], rank[prev + k] if prev + k < n else -1)
            cur_key = (rank[cur], rank[cur + k] if cur + k < n else -1)
            tmp[cur] = tmp[prev] + (prev_key != cur_key)
        rank = tmp[:]
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa

# Kasai's algorithm builds the LCP array in O(n): lcp[i] is the length
# of the longest common prefix of suffixes sa[i] and sa[i+1]. The key
# trick is that when we move to the next suffix, the shared prefix can
# only shrink by at most one, so we never re-scan from scratch.
def kasai_lcp(s, sa):
    n = len(s)
    rank = [0] * n
    for i, pos in enumerate(sa):
        rank[pos] = i
    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        r = rank[i]
        if r == n - 1:
            continue
        j = sa[r + 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[r] = h
        if h > 0:
            h -= 1
    return lcp

s = "banana"
sa = suffix_array(s)
print(sa)                          # [5, 3, 1, 0, 4, 2] - suffixes in order
print([s[i:] for i in sa])         # ['a', 'ana', 'anana', 'banana', 'na', 'nana']
lcp = kasai_lcp(s, sa)
print(lcp)                         # [1, 3, 0, 0, 2]

# Longest repeated substring: the biggest LCP value tells us the
# longest string that appears at least twice, and where it starts.
def longest_repeated_substring(s):
    sa = suffix_array(s)
    lcp = kasai_lcp(s, sa)
    best = max(lcp)
    i = lcp.index(best)
    return s[sa[i]:sa[i] + best]

print(longest_repeated_substring("banana"))   # 'ana'
print(longest_repeated_substring("abcababc"))  # 'abc'

# Suffix arrays and LCP matter for string problems: finding repeated
# substrings, longest common substrings, and pattern matching - the
# engine behind tools like diff, plagiarism checks, and DNA analysis.
