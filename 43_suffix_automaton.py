# Suffix automaton: all substrings of a string in a compact automaton

# A suffix automaton (SAM) is a small machine that accepts exactly the
# substrings of a string. It has at most 2n states for a string of
# length n, far fewer than listing every substring separately.
# Each state groups together substrings that end at the same places,
# and each state stores its longest length and a suffix link to the
# state for its longest proper suffix.

class SuffixAutomaton:
    def __init__(self):
        # state 0 is the start state: empty string, no link (-1)
        self.next = [{}]  # next[state][char] = next state
        self.link = [-1]
        self.length = [0]
        self.last = 0

    # add one character, extending the automaton
    def extend(self, ch):
        cur = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)
        p = self.last
        # every state on the suffix chain missing this edge gets it
        while p != -1 and ch not in self.next[p]:
            self.next[p][ch] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][ch]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                # clone q: same edges, shorter length, so the split is clean
                clone = len(self.next)
                self.next.append(self.next[q].copy())
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])
                while p != -1 and self.next[p].get(ch) == q:
                    self.next[p][ch] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur

    def build(self, s):
        for ch in s:
            self.extend(ch)

    # True if pattern appears anywhere in the original string
    def contains(self, pattern):
        state = 0
        for ch in pattern:
            if ch not in self.next[state]:
                return False
            state = self.next[state][ch]
        return True

    # each state adds (length - link length) brand-new substrings
    def distinct_substrings(self):
        total = 0
        for v in range(1, len(self.next)):
            total += self.length[v] - self.length[self.link[v]]
        return total


sam = SuffixAutomaton()
sam.build("ababa")
print(sam.contains("bab"))  # True ("ababa" contains "bab")
print(sam.contains("abc"))  # False
print(sam.distinct_substrings())  # 9 (a, b, ab, ba, aba, bab, abab, baba, ababa)

# ---
# Why it matters: one automaton answers substring questions in O(m) for
# a pattern of length m, and counts distinct substrings without listing
# them, which is why it is used in text search and bioinformatics.
