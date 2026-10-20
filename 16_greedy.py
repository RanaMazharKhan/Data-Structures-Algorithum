# Greedy algorithms: make the best local choice at each step and never look back

# Greedy works when a problem has the "greedy choice property": picking
# the best-looking option right now can never hurt the final answer.
# It is not always correct, but when it is, it is simple and fast.

# Coin change (canonical coin system): to use the fewest coins, always
# take the biggest coin that still fits. This is correct for coins like
# 1, 5, 10, 25 but fails for some weird coin systems (greedy's risk).
def min_coins(coins, amount):
    coins = sorted(coins, reverse=True)
    used = []
    for c in coins:
        while amount >= c:
            used.append(c)
            amount -= c
    return used

print(min_coins([1, 5, 10, 25], 63))  # [25, 25, 10, 1, 1, 1] - 6 coins

# Activity selection: pick the most activities that do not overlap.
# The greedy move is to always pick the activity that ends FIRST.
# Why it works: the activity ending earliest leaves the most room
# for everything after it.
def activity_selection(starts, ends):
    # sort activities by their end time
    acts = sorted(zip(starts, ends), key=lambda a: a[1])
    picked = []
    last_end = -1
    for s, e in acts:
        if s >= last_end:      # no clash with the last picked one
            picked.append((s, e))
            last_end = e
    return picked

print(activity_selection([1, 3, 0, 5, 8, 5], [2, 4, 6, 7, 9, 9]))
# [(1, 2), (3, 4), (5, 7), (8, 9)] - 4 non-overlapping activities

# Greedy matters because it is the "take the shortcut" strategy behind
# Huffman coding, minimum spanning trees (Kruskal's), and scheduling
# problems. Always ask first: "can a local best choice ruin the global
# best answer?" If no, greedy is the simplest correct solution.
