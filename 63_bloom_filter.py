# Bloom filter - a fast "maybe in the set?" test using tiny memory
# It uses a bit array and a few hash functions.
# It never says "no" wrongly, but sometimes says "maybe" by mistake.

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [0] * size

    # simple hash: mix the built-in hash with a seed
    def _hashes(self, item):
        out = []
        for seed in range(self.num_hashes):
            h = hash((item, seed)) % self.size
            out.append(h)
        return out

    # add an item: set all its hash positions to 1
    def add(self, item):
        for pos in self._hashes(item):
            self.bits[pos] = 1

    # check an item: "definitely not in" if any bit is 0,
    # "maybe in" if all its bits are 1
    def __contains__(self, item):
        return all(self.bits[pos] == 1 for pos in self._hashes(item))


# Example: store some usernames, then ask about new ones
bf = BloomFilter(size=100, num_hashes=3)
for name in ["ali", "sara", "usman", "fatima"]:
    bf.add(name)

print("ali" in bf)        # True - we added it
print("sara" in bf)       # True - we added it
print("bilal" in bf)      # False - definitely never added
print("zain" in bf)       # False (probably) - not added

# ---
# Why it matters: databases, caches and browsers use Bloom filters
# to skip expensive disk lookups. They answer "definitely not here"
# in constant time using only a few bits per item.
