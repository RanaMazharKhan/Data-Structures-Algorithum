# Palindromic tree (Eertree): count distinct palindromic substrings

# A palindromic tree stores every distinct palindrome in a string as
# one node. Each node knows its length and a suffix link to the longest
# proper palindromic suffix, so adding a new character only needs to
# follow links until the palindrome can be extended.
class PalindromicTree:
    def __init__(self):
        # Node 0: the odd root, length -1, so any single letter extends it.
        # Node 1: the even root, length 0, the empty palindrome.
        self.length = [-1, 0]
        self.link = [0, 0]
        self.next = [dict(), dict()]
        self.s = []
        self.last = 1

    # Find the longest suffix palindrome of the string so far that
    # can be extended by the new character on both sides.
    def _get_suffix(self, pos):
        while True:
            cur_len = self.length[self.last]
            if pos - 1 - cur_len >= 0 and self.s[pos - 1 - cur_len] == self.s[pos]:
                return self.last
            self.last = self.link[self.last]

    # Add one character. Either the new palindrome already exists as a
    # node, or we create a node for it and set its suffix link.
    def add_char(self, ch):
        self.s.append(ch)
        pos = len(self.s) - 1
        cur = self._get_suffix(pos)
        if ch in self.next[cur]:
            self.last = self.next[cur][ch]
            return False
        new = len(self.length)
        self.length.append(self.length[cur] + 2)
        self.next.append(dict())
        self.link.append(0)
        self.next[cur][ch] = new
        if self.length[new] == 1:
            self.link[new] = 1
        else:
            self.last = self.link[cur]
            self.last = self._get_suffix(pos)
            self.link[new] = self.next[self.last][ch]
        self.last = new
        return True

    # The two roots are not real palindromes, so distinct
    # palindromes = nodes minus 2.
    def distinct_palindromes(self):
        return len(self.length) - 2


def count_distinct_palindromes(s):
    tree = PalindromicTree()
    for ch in s:
        tree.add_char(ch)
    return tree.distinct_palindromes()


print(count_distinct_palindromes("ababa"))   # 5: a, b, aba, bab, ababa
print(count_distinct_palindromes("aaa"))     # 3: a, aa, aaa
print(count_distinct_palindromes("abc"))     # 3: a, b, c

# Longest palindromic substring is just the longest node: each node
# stores its length, so scan them and keep the biggest.
def longest_palindrome_length(s):
    tree = PalindromicTree()
    for ch in s:
        tree.add_char(ch)
    return max(tree.length)

print(longest_palindrome_length("babad"))  # 3, "bab" or "aba"
print(longest_palindrome_length("cbbd"))   # 2, "bb"

# Why it matters: counting distinct palindromes by brute force checks
# every substring, which is slow. The eertree does it in linear time
# and is the standard tool for palindrome counting, longest palindromic
# substring, and palindromic factorisation in string problems.
