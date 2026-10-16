# Hash table - how Python dict lookups are instant even with millions of keys

# A hash table is a fixed-size list of "buckets". A hash function turns a
# key into a bucket index: index = hash(key) % size. Lookup is then just
# one jump to that bucket - O(1) on average, no searching needed.
def simple_hash(key, size):
    return sum(ord(c) for c in str(key)) % size


# Collision: two different keys land in the same bucket.
# Chaining fixes it - each bucket holds a small list of (key, value) pairs,
# and we scan only that tiny list.
class HashTable:
    def __init__(self, size=8):
        self.buckets = [[] for _ in range(size)]
        self.size = size

    def _index(self, key):
        return simple_hash(key, self.size)

    # put: hash the key, find the bucket, add or update the pair
    def put(self, key, value):
        bucket = self.buckets[self._index(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)   # key exists -> update
                return
        bucket.append((key, value))        # new key -> append

    # get: hash the key and check only that bucket's small list
    def get(self, key):
        bucket = self.buckets[self._index(key)]
        for k, v in bucket:
            if k == key:
                return v
        return None                        # key not found

    def show_buckets(self):
        for i, b in enumerate(self.buckets):
            print(i, b)


ht = HashTable(size=8)
ht.put("apple", 5)
ht.put("banana", 3)
ht.put("orange", 8)
print(ht.get("apple"))    # 5
print(ht.get("banana"))   # 3
print(ht.get("grape"))    # None

# Collisions in action: "ab" and "ba" hash to the same bucket with our
# simple hash, but chaining keeps both values safe.
ht.put("ab", "first")
ht.put("ba", "second")
print(ht.get("ab"), ht.get("ba"))   # first second
print("--- bucket layout ---")
ht.show_buckets()


# Why it matters: dicts and sets are hash tables, and they are behind
# caches, database indexes, word-frequency counters and login sessions.
# The chaining idea also explains why a BAD hash function (too many
# collisions) turns O(1) lookups into slow list scans.
