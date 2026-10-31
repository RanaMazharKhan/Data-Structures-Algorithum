# B-tree: a balanced tree for disks and databases

# A binary search tree keeps one key per node, so it grows tall and
# each level can mean a slow disk read. A B-tree stores many keys per
# node and stays short and wide, which is why databases and file
# systems use it. Here t = 2, so each node holds at most 3 keys.
class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf

    # Search this subtree for key, like binary search in each node.
    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and self.keys[i] == key:
            return True
        if self.leaf:
            return False
        return self.children[i].search(key)

    # Insert into a node that is guaranteed not full.
    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(0)
            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and self.keys[i] > key:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 3:
                self.split_child(i)
                if self.keys[i] < key:
                    i += 1
            self.children[i].insert_non_full(key)

    # Split a full child into two nodes and lift its middle key up.
    def split_child(self, i):
        t = 2
        full = self.children[i]
        new = BTreeNode(leaf=full.leaf)
        self.children.insert(i + 1, new)
        self.keys.insert(i, full.keys[t - 1])
        new.keys = full.keys[t:]
        full.keys = full.keys[:t - 1]
        if not full.leaf:
            new.children = full.children[t:]
            full.children = full.children[:t]


class BTree:
    def __init__(self):
        self.root = BTreeNode(leaf=True)

    def search(self, key):
        return self.root.search(key)

    # If the root is full, grow a new root first so the tree stays balanced.
    def insert(self, key):
        root = self.root
        if len(root.keys) == 3:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            new_root.split_child(0)
            self.root = new_root
        self.root.insert_non_full(key)

    # Print the keys level by level, so the wide shape is visible.
    def show(self):
        level = [self.root]
        while level:
            print([node.keys for node in level])
            nxt = []
            for node in level:
                nxt.extend(node.children)
            level = nxt


# Example: insert enough keys to force splits, then search
tree = BTree()
for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    tree.insert(key)
tree.show()
print(tree.search(6))   # True
print(tree.search(15))  # False

# Why it matters: B-trees keep data balanced with very few levels, so
# databases and file systems find records with very few disk reads.
