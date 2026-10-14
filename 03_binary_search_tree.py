# Binary Search Tree (BST) - a tree that keeps data sorted
# Rule: left child < parent < right child.
# This makes search/insert/delete O(log n) on average.

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # insert a value in the right place
    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if node is None:
            return Node(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        return node

    # search: True if the value exists
    def search(self, val):
        node = self.root
        while node:
            if val == node.val:
                return True
            node = node.left if val < node.val else node.right
        return False

    # inorder traversal prints values in sorted order
    def inorder(self):
        out = []
        self._inorder(self.root, out)
        return out

    def _inorder(self, node, out):
        if node:
            self._inorder(node.left, out)
            out.append(node.val)
            self._inorder(node.right, out)


# Example: insert numbers, then read them back sorted
t = BST()
for x in [50, 30, 70, 20, 40, 60, 80]:
    t.insert(x)

print(t.inorder())        # [20, 30, 40, 50, 60, 70, 80] - sorted!
print(t.search(40))       # True
print(t.search(100))      # False

# ---
# Why it matters: a BST is the idea behind database indexes and
# sets/maps in many languages. Balanced versions (AVL, Red-Black)
# keep it O(log n) even in the worst case.
