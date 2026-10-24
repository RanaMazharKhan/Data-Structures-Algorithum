# Aho-Corasick: search MANY patterns in one text in a single pass
# Idea: build a trie of all patterns, then add "fail links" that work
# like KMP's prefix links - when a character does not match, the fail
# link tells you the longest suffix of what you saw that is still a
# valid trie prefix, so you never move backwards in the text.

class Node:
    def __init__(self):
        self.children = {}     # char -> Node
        self.fail = None       # where to go on mismatch
        self.words = []        # patterns that end at this node


class AhoCorasick:
    def __init__(self, patterns):
        self.root = Node()
        # step 1: put every pattern in the trie
        for p in patterns:
            node = self.root
            for ch in p:
                node = node.children.setdefault(ch, Node())
            node.words.append(p)
        # step 2: build fail links with a BFS
        queue = []
        for node in self.root.children.values():
            node.fail = self.root
            queue.append(node)
        while queue:
            cur = queue.pop(0)
            for ch, nxt in cur.children.items():
                queue.append(nxt)
                f = cur.fail
                while f is not None and ch not in f.children:
                    f = f.fail
                nxt.fail = f.children[ch] if f else self.root
                nxt.words += nxt.fail.words  # inherit matches

    # step 3: walk the text once, follow fail links on mismatch
    def search(self, text):
        found = []
        node = self.root
        for i, ch in enumerate(text):
            while node is not None and ch not in node.children:
                node = node.fail
            node = node.children[ch] if node else self.root
            for w in node.words:
                found.append((w, i - len(w) + 1))  # (pattern, start index)
        return found


# Example: find several banned words in one line of chat
patterns = ["he", "she", "his", "hers"]
ac = AhoCorasick(patterns)
hits = ac.search("shis he is here")
for word, pos in hits:
    print(f"found '{word}' at index {pos}")
# found 'his' at index 1, 'he' at index 5, 'he' at index 11

# ---
# Why it matters: with k patterns and a text of length n this runs in
# O(n + total matches) instead of running KMP k times. Used in virus
# scanners, spam filters and plagiarism checkers that scan one input
# against thousands of patterns at once.
