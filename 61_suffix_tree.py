# Suffix tree: fast substring search

# A suffix tree stores every suffix of a text in one compressed trie.
# Suffixes that share a start share an edge, and edges are labelled with
# whole chunks of text instead of single letters, so the tree stays small.
# Once it is built, searching for a pattern means walking down its letters
# and never scanning the whole text again.
class Node:
    def __init__(self):
        self.children = {}
        self.index = None


class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.root = Node()
        for start in range(len(text)):
            self.insert(text[start:], start)

    # Insert one suffix, splitting an edge when it only partly matches.
    def insert(self, suffix, start):
        node = self.root
        i = 0
        while i < len(suffix):
            ch = suffix[i]
            if ch not in node.children:
                leaf = Node()
                leaf.index = start
                node.children[ch] = (suffix[i:], leaf)
                return
            label, child = node.children[ch]
            j = 0
            while j < len(label) and i + j < len(suffix) and label[j] == suffix[i + j]:
                j += 1
            if j == len(label):
                node = child
                i += j
                continue
            middle = Node()
            middle.children[label[j]] = (label[j:], child)
            node.children[ch] = (label[:j], middle)
            if i + j == len(suffix):
                middle.index = start
                return
            leaf = Node()
            leaf.index = start
            middle.children[suffix[i + j]] = (suffix[i + j:], leaf)
            return
        node.index = start

    # Walk the pattern down the edges; a mismatch means it is absent.
    def search(self, pattern):
        node = self.root
        i = 0
        while i < len(pattern):
            ch = pattern[i]
            if ch not in node.children:
                return False
            label, child = node.children[ch]
            j = 0
            while j < len(label) and i + j < len(pattern) and label[j] == pattern[i + j]:
                j += 1
            if j == len(label):
                node = child
                i += j
            elif i + j == len(pattern):
                return True
            else:
                return False
        return True

    # Collect every suffix start stored under a node.
    def collect(self, node, found):
        if node.index is not None:
            found.append(node.index)
        for label, child in node.children.values():
            self.collect(child, found)

    # Find all start positions of a pattern, by collecting under its end node.
    def occurrences(self, pattern):
        node = self.root
        i = 0
        while i < len(pattern):
            ch = pattern[i]
            if ch not in node.children:
                return []
            label, child = node.children[ch]
            j = 0
            while j < len(label) and i + j < len(pattern) and label[j] == pattern[i + j]:
                j += 1
            if j == len(label):
                node = child
                i += j
            elif i + j == len(pattern):
                found = []
                self.collect(child, found)
                return sorted(found)
            else:
                return []
        found = []
        self.collect(node, found)
        return sorted(found)

    # Print the edges, so the shared prefixes are visible.
    def show(self, node=None, prefix=""):
        if node is None:
            node = self.root
        for label, child in node.children.values():
            print(prefix + label, "(suffix", str(child.index) + ")" if child.index is not None else "")
            self.show(child, prefix + "  ")


# Example: build the tree for "banana" and search inside it
tree = SuffixTree("banana")
tree.show()
print(tree.search("ana"))    # True
print(tree.search("nan"))    # True
print(tree.search("apple"))  # False
print(tree.occurrences("ana"))  # [1, 3]
print(tree.occurrences("na"))   # [2, 4]

# Why it matters: suffix trees answer substring, repeat and longest-common
# substring questions in time proportional to the pattern, not the text,
# and they power genome search and plagiarism detection.
