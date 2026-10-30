# Splay tree: a self-adjusting binary search tree

# A splay tree is a BST with one special rule: every time you access a node
# (search or insert), you "splay" it - rotate it all the way up to the root.
# Recently used items therefore sit near the top, so repeated access to the
# same items is fast. This is called the move-to-front idea, and it works
# great when some items are used much more often than others.
# Splaying uses three rotation patterns, based on the node and its parent:
# zig (parent is root), zig-zig (both lean the same way), zig-zag (they lean
# opposite ways). Repeating these moves the node to the root step by step.
class Node:
    def __init__(self, key):
        self.key = key
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


def splay(root, key):
    if root is None or root.key == key:
        return root
    if key < root.key:
        if root.left is None:
            return root
        if key < root.left.key:  # zig-zig: rotate right twice
            root.left.left = splay(root.left.left, key)
            root = rotate_right(root)
        elif key > root.left.key:  # zig-zag: left then right
            root.left.right = splay(root.left.right, key)
            if root.left.right is not None:
                root.left = rotate_left(root.left)
        return rotate_right(root) if root.left is not None else root
    else:
        if root.right is None:
            return root
        if key > root.right.key:  # zig-zig: rotate left twice
            root.right.right = splay(root.right.right, key)
            root = rotate_left(root)
        elif key < root.right.key:  # zig-zag: right then left
            root.right.left = splay(root.right.left, key)
            if root.right.left is not None:
                root.right = rotate_right(root.right)
        return rotate_left(root) if root.right is not None else root


def insert(root, key):
    if root is None:
        return Node(key)
    root = splay(root, key)
    if root.key == key:
        return root  # already present
    node = Node(key)
    if key < root.key:
        node.right = root
        node.left = root.left
        root.left = None
    else:
        node.left = root
        node.right = root.right
        root.right = None
    return node


def search(root, key):
    root = splay(root, key)
    return root, (root is not None and root.key == key)


def inorder(root, out):
    if root is not None:
        inorder(root.left, out)
        out.append(root.key)
        inorder(root.right, out)


root = None
for key in [10, 20, 30, 40, 50]:
    root = insert(root, key)
print("root after inserts:", root.key)  # 50 (last inserted splayed to top)
root, found = search(root, 20)
print("search 20:", found, "| new root:", root.key)  # True, root is now 20
root, found = search(root, 20)
print("search 20 again:", found, "| root still:", root.key)  # already at top, instant
result = []
inorder(root, result)
print("inorder (sorted):", result)  # [10, 20, 30, 40, 50]

# Why it matters: splay trees adapt to how you actually use data - hot items
# stay near the root. They are used in caches, memory allocators, and
# anywhere access patterns are skewed toward a few popular items.
