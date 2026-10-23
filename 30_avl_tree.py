# AVL Tree - a binary search tree that stays balanced by itself
# Rule: every node's left and right subtree heights differ by at most 1.
# After insert, the tree rotates the unbalanced node back into balance.

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1  # leaf height is 1


def height(n):
    return n.height if n else 0


def balance_factor(n):
    return height(n.left) - height(n.right)


# rotate right: x's left child y takes x's place
def rotate_right(x):
    y = x.left
    x.left = y.right
    y.right = x
    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y


# rotate left: mirror of rotate right
def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))
    return y


def insert(node, val):
    if node is None:
        return Node(val)
    if val < node.val:
        node.left = insert(node.left, val)
    else:
        node.right = insert(node.right, val)
    node.height = 1 + max(height(node.left), height(node.right))

    # fix the imbalance (4 cases)
    b = balance_factor(node)
    if b > 1 and val < node.left.val:    # left-left
        return rotate_right(node)
    if b < -1 and val > node.right.val:  # right-right
        return rotate_left(node)
    if b > 1:                            # left-right
        node.left = rotate_left(node.left)
        return rotate_right(node)
    if b < -1:                           # right-left
        node.right = rotate_right(node.right)
        return rotate_left(node)
    return node


# inorder traversal reads values back sorted
def inorder(node, out):
    if node:
        inorder(node.left, out)
        out.append(node.val)
        inorder(node.right, out)


# Example: insert sorted numbers 1..7 (a plain BST would become a line)
root = None
for x in [1, 2, 3, 4, 5, 6, 7]:
    root = insert(root, x)

vals = []
inorder(root, vals)
print(vals)                 # [1, 2, 3, 4, 5, 6, 7] - sorted
print(height(root))         # 3 - balanced, not 7!

# ---
# Why it matters: AVL guarantees O(log n) search, insert and delete by
# never letting the tree grow lopsided. Used in databases and file
# systems where lookups must stay fast no matter the insert order.
