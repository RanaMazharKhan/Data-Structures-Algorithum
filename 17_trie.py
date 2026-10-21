# Trie: a tree of letters for fast word lookup and autocomplete

# A trie stores words by sharing their common prefixes. Each node is
# one letter; following the letters of a word down from the root finds
# it. Looking up a word costs only as many steps as it has letters.

# each node holds its child letters and a flag for "a word ends here"
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # insert walks/creates one node per letter of the word
    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    # search walks down the letters; found only if a word ends there
    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_word

    # prefix check: is there any word that STARTS with this text?
    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    # autocomplete: collect every word below the prefix node
    def autocomplete(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        results = []
        def collect(n, word):
            if n.is_word:
                results.append(word)
            for ch, child in n.children.items():
                collect(child, word + ch)
        collect(node, prefix)
        return results

t = Trie()
for word in ["cat", "car", "cart", "dog", "door"]:
    t.insert(word)

print(t.search("car"))        # True - "car" was inserted
print(t.search("ca"))         # False - "ca" is only a prefix, not a word
print(t.starts_with("ca"))    # True - "cat"/"car"/"cart" start with "ca"
print(t.starts_with("do"))    # True
print(t.starts_with("z"))     # False
print(t.autocomplete("car"))  # ['car', 'cart'] - suggestions after typing "car"
print(t.autocomplete("d"))    # ['dog', 'door']

# Tries matter because they power autocomplete, spell checkers, and
# phone-keyboard word suggestions. Once built, searching or suggesting
# a word costs O(letters) - no scanning through a whole word list.
