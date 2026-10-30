# Treap: a randomized balanced binary search tree

# A treap is a BST by key AND a heap by priority. Each node gets a random
# priority when inserted; the tree keeps BST order on keys and heap order
# on priorities (parent priority smaller than children). Random priorities
# keep the tree balanced on average, so insert/search/delete stay O(log n)
# without the complex rebalancing rules of AVL or red-black trees.
# Insert: insert like a normal BST, then rotate the node up while its
# priority is smaller than its parent's - this restores the heap property.
import random


class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.left = None
        self.right = None


def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    return x


def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    return y


def insert(root, key):
    if root is None:
        return Node(key)
    if key == root.key:
        return root
    if key < root.key:
        root.left = insert(root.left, key)
        if root.left.priority < root.priority:
            root = rotate_right(root)
    else:
        root.right = insert(root.right, key)
        if root.right.priority < root.priority:
            root = rotate_left(root)
    return root


def search(root, key):
    while root is not None:
        if key == root.key:
            return True
        root = root.left if key < root.key else root.right
    return False


def inorder(root, out):
    if root is not None:
        inorder(root.left, out)
        out.append(root.key)
        inorder(root.right, out)


random.seed(42)  # fixed seed so the demo is the same every run
root = None
for key in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, key)
result = []
inorder(root, result)
print("inorder (sorted):", result)  # [20, 30, 40, 50, 60, 70, 80]
print("search 40:", search(root, 40))  # True
print("search 25:", search(root, 25))  # False

# Why it matters: treaps give you a balanced BST with very little code -
# the randomness does the balancing work for you. They are also the base
# for implicit treaps, which power fast sequence operations in editors.
