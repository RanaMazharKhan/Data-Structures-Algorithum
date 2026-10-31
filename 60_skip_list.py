# Skip list: a linked list with express lanes

# Searching a plain linked list is slow because you walk node by node.
# A skip list adds extra levels above it: a few nodes get promoted to
# a fast lane, a few of those to an even faster lane. Search starts at
# the top lane and drops down, like express lanes on a motorway.
# Levels are picked by coin flips, so the structure stays balanced
# on average without any rebalancing code.
import random

random.seed(0)

MAX_LEVEL = 4


class SkipNode:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)


class SkipList:
    def __init__(self):
        self.header = SkipNode(None, MAX_LEVEL)
        self.level = 0

    # Flip a coin for each extra level, up to the maximum.
    def random_level(self):
        level = 0
        while level < MAX_LEVEL and random.random() < 0.5:
            level += 1
        return level

    # Walk from the top lane down, skipping over smaller keys.
    def search(self, key):
        node = self.header
        for i in range(self.level, -1, -1):
            while node.forward[i] and node.forward[i].key < key:
                node = node.forward[i]
        node = node.forward[0]
        return node is not None and node.key == key

    # Remember where each level must be rewired, then insert.
    def insert(self, key):
        update = [None] * (MAX_LEVEL + 1)
        node = self.header
        for i in range(self.level, -1, -1):
            while node.forward[i] and node.forward[i].key < key:
                node = node.forward[i]
            update[i] = node
        new_level = self.random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        new_node = SkipNode(key, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    # Find the node on every level and unlink it.
    def delete(self, key):
        update = [None] * (MAX_LEVEL + 1)
        node = self.header
        for i in range(self.level, -1, -1):
            while node.forward[i] and node.forward[i].key < key:
                node = node.forward[i]
            update[i] = node
        target = node.forward[0]
        if target and target.key == key:
            for i in range(len(target.forward)):
                if update[i].forward[i] == target:
                    update[i].forward[i] = target.forward[i]
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

    # Print each level from top to bottom, so the lanes are visible.
    def show(self):
        for i in range(self.level, -1, -1):
            keys = []
            node = self.header.forward[i]
            while node:
                keys.append(node.key)
                node = node.forward[i]
            print("level", i, ":", keys)


# Example: insert, search, delete, and look at the lanes
skip = SkipList()
for key in [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]:
    skip.insert(key)
skip.show()
print(skip.search(19))  # True
print(skip.search(15))  # False
skip.delete(19)
print(skip.search(19))  # False after deleting
skip.show()

# Why it matters: skip lists give balanced-tree speed with much simpler
# code, and they are used in real systems like Redis sorted sets.
