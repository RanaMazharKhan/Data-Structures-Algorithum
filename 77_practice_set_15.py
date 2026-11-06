# Practice set 15: mixed problems from all topics so far

# Problem 1: maximum xor of any subset, using a linear basis.
# Keep one basis vector per bit position. Inserting a number
# cancels its highest bit, so the basis stays tiny but can
# build every xor the whole set can build.
class XorBasis:
    def __init__(self):
        self.basis = [0] * 31

    def insert(self, x):
        while x:
            bit = x.bit_length() - 1
            if self.basis[bit] == 0:
                self.basis[bit] = x
                return
            x ^= self.basis[bit]

    def max_xor(self):
        ans = 0
        for bit in range(30, -1, -1):
            if ans ^ self.basis[bit] > ans:
                ans ^= self.basis[bit]
        return ans

basis = XorBasis()
for x in [3, 10, 5, 25, 2, 8]:
    basis.insert(x)
print(basis.max_xor())  # 31, the best xor any subset can reach

# Problem 2: count numbers in a range with binary search.
# Sorting once lets bisect answer "how many values are between
# l and r" in log time, the same idea a wavelet tree uses
# to answer range counts on any slice of an array.
import bisect

nums = [1, 3, 5, 5, 7, 9, 11]
left = bisect.bisect_left(nums, 5)
right = bisect.bisect_right(nums, 7)
print(right - left)  # 3, the values 5, 5, 7 lie in [5, 7]

# Problem 3: longest palindromic substring by expanding around centres.
# Every palindrome has a centre. Try each centre, expand while the
# letters match, and keep the longest stretch you find.
def longest_palindrome(s):
    best = ""
    for centre in range(len(s)):
        for start, end in [(centre, centre), (centre, centre + 1)]:
            while start >= 0 and end < len(s) and s[start] == s[end]:
                if end - start + 1 > len(best):
                    best = s[start:end + 1]
                start -= 1
                end += 1
    return best

print(longest_palindrome("babad"))  # "bab" (or "aba"), length 3

# Problem 4: count distinct substrings using a suffix automaton.
# A suffix automaton is a small graph that contains every substring
# of a string. Each state stands for a set of substrings, and the
# length difference between a state and its link counts how many
# new substrings that state adds.
class SuffixAutomaton:
    def __init__(self):
        self.next = [{}]
        self.link = [-1]
        self.length = [0]
        self.last = 0

    def extend(self, ch):
        cur = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)
        p = self.last
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
                clone = len(self.next)
                self.next.append(dict(self.next[q]))
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])
                while p != -1 and self.next[p].get(ch) == q:
                    self.next[p][ch] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur

    def distinct_substrings(self):
        total = 0
        for v in range(1, len(self.next)):
            total += self.length[v] - self.length[self.link[v]]
        return total

sam = SuffixAutomaton()
for ch in "ababa":
    sam.extend(ch)
print(sam.distinct_substrings())  # 9 distinct substrings

# Problem 5: kth smallest element in a stream using a max-heap trick.
# Python only has a min-heap, so store negative numbers. The heap
# keeps the k smallest, and its top is the kth smallest so far.
import heapq

def kth_smallest_stream(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, -x)
        if len(heap) > k:
            heapq.heappop(heap)
    return -heap[0]

print(kth_smallest_stream([7, 10, 4, 3, 20, 15], 3))  # 7

# Why it matters: real problems rarely say which topic they are.
# Practice sets train you to recognise the pattern first, then
# pick the right structure, instead of memorising one trick at a time.
