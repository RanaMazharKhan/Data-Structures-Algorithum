# LRU cache: remember the most recent, forget the least recent
# A hash map gives O(1) lookup of any key, and a doubly linked list
# tracks use order: most recently used at the front, least recent at
# the tail. On a hit or a set, the node moves to the front; when the
# cache is full, the tail node is evicted.

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}                    # key -> Node
        self.head = Node(None, None)     # dummy front
        self.tail = Node(None, None)     # dummy back
        self.head.next = self.tail
        self.tail.prev = self.head

    # unhook a node from the list
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    # insert right after the dummy head (most recent spot)
    def _push_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)        # refresh: most recently used
        self._push_front(node)
        return node.val

    def put(self, key, val):
        if key in self.map:      # update an existing key
            self._remove(self.map[key])
        node = Node(key, val)
        self.map[key] = node
        self._push_front(node)
        if len(self.map) > self.capacity:
            old = self.tail.prev  # least recently used
            self._remove(old)
            del self.map[old.key]


# Example: capacity 2
cache = LRUCache(2)
cache.put("a", 1)         # cache: a
cache.put("b", 2)         # cache: b, a
print(cache.get("a"))     # 1, cache: a, b  ('a' is now most recent)
cache.put("c", 3)         # full -> evicts 'b'. cache: c, a
print(cache.get("b"))     # -1 (evicted)
print(cache.get("c"))     # 3

# ---
# Why it matters: LRU is the classic page-replacement policy. Web
# browsers, CDNs and database buffer pools use it so the limited memory
# keeps the hottest data and drops whatever was not asked for lately.
