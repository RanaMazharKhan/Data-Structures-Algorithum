# k-d tree: nearest neighbour search in many dimensions

# A k-d tree is a binary tree for points in k dimensions.
# At each level we split on a different axis: level 0 splits on x,
# level 1 on y, level 2 on x again, and so on. Each node stores one
# point, with smaller values on the left and larger on the right.
class KDNode:
    def __init__(self, point, axis):
        self.point = point
        self.axis = axis
        self.left = None
        self.right = None


# Build the tree: pick the median point on the current axis, so the
# tree stays balanced, then build the left and right halves the same way.
def build(points, depth=0):
    if not points:
        return None
    k = len(points[0])
    axis = depth % k
    points = sorted(points, key=lambda p: p[axis])
    mid = len(points) // 2
    node = KDNode(points[mid], axis)
    node.left = build(points[:mid], depth + 1)
    node.right = build(points[mid + 1:], depth + 1)
    return node


points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
tree = build(points)
print("root:", tree.point)  # median on x axis

# Nearest neighbour: walk down to the leaf nearest the target, then
# backtrack. If the other side of a split could hold a closer point
# (its distance to the splitting line beats our best), search it too.
def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def nearest(node, target, best=None):
    if node is None:
        return best
    if best is None or distance(target, node.point) < distance(target, best):
        best = node.point
    axis = node.axis
    near = node.left if target[axis] < node.point[axis] else node.right
    far = node.right if near is node.left else node.left
    best = nearest(near, target, best)
    # Only check the far side if it could beat the current best.
    if abs(target[axis] - node.point[axis]) < distance(target, best):
        best = nearest(far, target, best)
    return best


print(nearest(tree, (9, 2)))  # (8, 1), the closest point
print(nearest(tree, (3, 5)))  # one of the equally close points

# Why it matters: searching every point is slow when there are millions.
# k-d trees power nearest-neighbour search in maps, image search,
# recommendation systems and robotics, where close points matter.
