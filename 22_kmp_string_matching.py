# KMP string matching: find a pattern in text without ever re-scanning

# Naive search restarts from the next character after every mismatch,
# which re-scans characters it already looked at. KMP is smarter: it
# first studies the PATTERN and builds a "prefix table" (LPS) that
# records, for each position, the length of the longest proper prefix
# which is also a suffix. On a mismatch, that table says exactly how
# far the pattern can shift forward without re-checking matched text.

# Building the LPS table: walk the pattern once, keep a pointer `length`
# for the current match. On a match, grow it; on a mismatch, fall back
# using the table itself instead of starting over.
def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    for i in range(1, len(pattern)):
        while length > 0 and pattern[i] != pattern[length]:
            length = lps[length - 1]     # fall back, do not restart
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
    return lps

print(build_lps("aabaa"))  # [0, 1, 0, 1, 2] - prefix "aa" repeats at the end

# The search: scan the text once. Matched characters advance both the
# text pointer and the pattern pointer; a mismatch falls back the
# pattern pointer using the LPS table, so text is never re-scanned.
def kmp_search(text, pattern):
    lps = build_lps(pattern)
    j = 0             # position inside the pattern
    matches = []
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = lps[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):            # full pattern matched
            matches.append(i - j + 1)
            j = lps[j - 1]               # keep going for overlapping hits
    return matches

print(kmp_search("ababcababcabc", "ababc"))   # [0, 5]
print(kmp_search("aaaa", "aa"))              # [0, 1, 2] - overlaps found

# Compare with naive search on the same input to see the same answer:
def naive_search(text, pattern):
    hits = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i + len(pattern)] == pattern:
            hits.append(i)
    return hits

print(naive_search("aaaa", "aa"))  # [0, 1, 2] - same, but O(n*m)

# KMP matters because it turns text search into one linear pass:
# Ctrl+F in editors, plagiarism detectors, DNA sequence search, and
# intrusion-detection systems that scan network traffic for attack
# patterns all rely on this "never re-scan" idea.
