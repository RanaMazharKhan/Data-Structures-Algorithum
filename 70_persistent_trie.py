# Persistent trie: versioned prefix queries

# A normal trie stores words letter by letter, but changing it loses
# the old version. A persistent trie never edits old nodes: every
# insert copies only the nodes on the new word's path, and all other
# nodes are shared. So each version stays frozen and usable forever.
class Node:
    def __init__(self, count=0):
        self.count = count  # how many words pass through this node
        self.child = {}     # letter -> Node


# Insert word into the trie rooted at prev and return the NEW root.
# Old nodes are copied, never changed, so prev still points to the
# old version exactly as it was.
def insert(prev, word, i=0):
    node = Node((prev.count + 1) if prev else 1)
    if prev:
        node.child = dict(prev.child)
    if i < len(word):
        ch = word[i]
        old_child = prev.child.get(ch) if prev else None
        node.child[ch] = insert(old_child, word, i + 1)
    return node


# Count how many words in this version start with prefix.
def count_prefix(root, prefix):
    node = root
    for ch in prefix:
        if node is None or ch not in node.child:
            return 0
        node = node.child[ch]
    return node.count


# Build one version per word, keeping every version in a list.
empty = Node()
versions = [empty]
for word in ["apple", "app", "apricot"]:
    versions.append(insert(versions[-1], word))

print(count_prefix(versions[1], "app"))  # 1, only "apple" exists yet
print(count_prefix(versions[2], "app"))  # 2, "apple" and "app"
print(count_prefix(versions[3], "ap"))   # 3, all three start with "ap"
print(count_prefix(versions[2], "apr"))  # 0, "apricot" is not in version 2
print(count_prefix(versions[3], "apr"))  # 1, "apricot" arrived in version 3
print(count_prefix(versions[1], "ap"))   # 1, version 1 is still unchanged

# Why it matters: versioned autocomplete, undo history and "what did
# the data look like yesterday?" queries all need old versions kept.
# Persistence gives you that without copying the whole structure.
