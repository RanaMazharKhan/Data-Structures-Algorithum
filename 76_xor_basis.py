# Linear basis: maximum xor subset queries

# XOR has a neat trick: from a set of numbers you can build a small
# basis, one number per bit position, that can make every xor the
# original set can make. The basis is tiny, at most one per bit.
class XorBasis:
    def __init__(self, max_bit=20):
        self.basis = [0] * (max_bit + 1)

    # Insert x: cancel its highest set bit with the basis vector for
    # that bit. If nothing is left, x was already representable.
    def insert(self, x):
        while x:
            bit = x.bit_length() - 1
            if self.basis[bit] == 0:
                self.basis[bit] = x
                return True
            x ^= self.basis[bit]
        return False

    # Check whether x can be formed by xoring some subset together.
    # Reducing x with the basis leaves 0 exactly when it can.
    def can_make(self, x):
        while x:
            bit = x.bit_length() - 1
            if self.basis[bit] == 0:
                return False
            x ^= self.basis[bit]
        return True

    # Build the biggest xor possible: try to improve the answer
    # from the highest bit down, keeping a change only if it helps.
    def max_xor(self):
        ans = 0
        for bit in range(len(self.basis) - 1, -1, -1):
            if ans ^ self.basis[bit] > ans:
                ans ^= self.basis[bit]
        return ans


basis = XorBasis()
for x in [3, 10, 5, 25, 2, 8]:
    basis.insert(x)

print(basis.max_xor())    # 31, the best xor any subset can reach
print(basis.can_make(7))  # True, some subset xors to 7
print(basis.can_make(1))  # True, some subset xors to 1

# A fresh basis over just [10, 5] shows the same idea on a tiny set.
small = XorBasis()
small.insert(10)
small.insert(5)
print(small.max_xor())    # 15, which is 10 xor 5

# Why it matters: maximum xor subset is a classic interview problem,
# and the same basis trick powers problems about xor queries, game
# states and spanning trees in xor graphs, all in very little code.
