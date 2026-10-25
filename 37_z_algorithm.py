# Z-algorithm: find every match of a pattern in linear time
# The Z-array of a string holds, at each position, the length of the
# longest prefix match starting there. Once you have it, searching a
# pattern in a text is just one pass over pattern + "$" + text.
# The trick: a Z-box (l, r) remembers a prefix match already found,
# so positions inside it can copy answers instead of rescanning.

def z_array(s):
    z = [0] * len(s)
    l = r = 0
    for i in range(1, len(s)):
        if i <= r:
            # i sits inside a known Z-box, reuse its answer
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


print(z_array("aabcaabxaaaz"))
# [0, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0]


# pattern search: a full-length match in the combined string marks a hit
def find_pattern(text, pattern):
    combined = pattern + "$" + text
    z = z_array(combined)
    hits = []
    for i in range(len(pattern) + 1, len(combined)):
        if z[i] == len(pattern):
            hits.append(i - len(pattern) - 1)
    return hits


print(find_pattern("aabcaabxaaaz", "aab"))   # [0, 4]
print(find_pattern("aaaaa", "aa"))           # [0, 1, 2, 3]

# ---
# Why it matters: the Z-algorithm powers fast substring search in
# text editors, plagiarism checkers and DNA sequence matching, and it
# runs in O(n) time because no character is ever compared twice.
