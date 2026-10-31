# Link-cut tree: a dynamic forest that can link, cut and query paths fast

# A forest is a set of trees. Normally changing a tree (linking or cutting
# an edge) is slow if we rebuild everything. A link-cut tree keeps each
# tree as a set of preferred paths stored in splay trees, so link, cut
# and path queries all run in about log n time.
class Node:
    def __init__(self, value):
        self.value = value
        self.sum = value
        self.left = None
        self.right = None
        self.parent = None
        self.rev = False


# A node is the root of its splay tree if its parent does not point
# to it as a left or right child.
def is_root(x):
    return x.parent is None or (x.parent.left != x and x.parent.right != x)


# Push the lazy reverse flag down to the children.
def push(x):
    if x.rev:
        x.left, x.right = x.right, x.left
        if x.left:
            x.left.rev = not x.left.rev
        if x.right:
            x.right.rev = not x.right.rev
        x.rev = False


# Recompute the subtree sum after a change.
def update(x):
    x.sum = x.value
    if x.left:
        x.sum += x.left.sum
    if x.right:
        x.sum += x.right.sum


# One splay rotation: lift x above its parent.
def rotate(x):
    p = x.parent
    g = p.parent
    if p.left == x:
        p.left = x.right
        if x.right:
            x.right.parent = p
        x.right = p
    else:
        p.right = x.left
        if x.left:
            x.left.parent = p
        x.left = p
    p.parent = x
    x.parent = g
    if g and not is_root(p):
        if g.left == p:
            g.left = x
        else:
            g.right = x
    update(p)
    update(x)


# Splay: bring x to the root of its splay tree with rotations.
def splay(x):
    stack = [x]
    y = x
    while not is_root(y):
        y = y.parent
        stack.append(y)
    while stack:
        push(stack.pop())
    while not is_root(x):
        p = x.parent
        g = p.parent
        if not is_root(p):
            if (p.left == x) == (g.left == p):
                rotate(p)
            else:
                rotate(x)
        rotate(x)


# Access: make the path from the tree root to x the preferred path,
# and bring x to the top. After this, x's right subtree is empty and
# the whole root-to-x path is in x's splay tree.
def access(x):
    last = None
    y = x
    while y:
        splay(y)
        y.right = last
        update(y)
        last = y
        y = y.parent
    splay(x)


# Make x the root of its represented tree, by reversing the path to it.
def make_root(x):
    access(x)
    x.rev = not x.rev


# Find the root of the tree that holds x.
def find_root(x):
    access(x)
    while True:
        push(x)
        if x.left:
            x = x.left
        else:
            break
    splay(x)
    return x


# Two nodes are connected if they share the same tree root.
def connected(x, y):
    return find_root(x) == find_root(y)


# Link: join two different trees with an edge between x and y.
def link(x, y):
    make_root(x)
    if find_root(y) != x:
        x.parent = y


# Cut: remove the edge between x and y, if it exists.
def cut(x, y):
    make_root(x)
    access(y)
    if y.left == x:
        y.left.parent = None
        y.left = None
        update(y)


# Path sum: after making x the root and accessing y, y's splay tree
# holds exactly the nodes on the x-to-y path.
def path_sum(x, y):
    make_root(x)
    access(y)
    return y.sum


# Example: build a chain 1 - 2 - 3 - 4, then query and change it
a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)
link(a, b)
link(b, c)
link(c, d)
print(connected(a, d))   # True, all in one tree
print(path_sum(a, d))    # 10 = 1 + 2 + 3 + 4
cut(b, c)
print(connected(a, d))   # False, the tree split in two
print(path_sum(a, b))    # 3 = 1 + 2
link(b, d)
print(connected(a, d))   # True again, through the new edge
print(path_sum(a, d))    # 7 = 1 + 2 + 4

# Why it matters: dynamic forests appear in network routing and
# dynamic connectivity problems, where edges come and go and we still
# need fast path queries. Link-cut trees are the standard tool for that.
