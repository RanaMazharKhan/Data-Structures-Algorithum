# Hilbert order Mo's algorithm: answer many range queries offline, faster than plain Mo's

# Mo's algorithm answers range queries by sliding a window [l, r] and
# adding/removing one element at a time. Plain Mo's sorts queries in
# blocks, which makes the window jump around a lot. Hilbert order
# sorts the queries along a space-filling curve instead, so the window
# moves much less in total - often 2-3x faster in practice.
def hilbert_order(x, y, power=21, rotate=0):
    if power == 0:
        return 0
    h = 1 << (power - 1)
    seg = 0
    if x < h:
        if y < h:
            seg = 0
        else:
            seg = 1
    else:
        if y < h:
            seg = 3
        else:
            seg = 2
    seg = (seg + rotate) & 3
    rotate_delta = [3, 0, 0, 1]
    nx = x & (h - 1)
    ny = y & (h - 1)
    nrot = (rotate + rotate_delta[seg]) & 3
    sub_square = 1 << (2 * power - 2)
    return seg * sub_square + hilbert_order(nx, ny, power - 1, nrot)

# Example query: count distinct numbers in each range [l, r]
def distinct_in_ranges(arr, queries):
    order = sorted(range(len(queries)),
                   key=lambda i: hilbert_order(queries[i][0], queries[i][1]))
    freq = {}
    distinct = 0
    answers = [0] * len(queries)
    l, r = 0, -1                    # current window is empty

    def add(i):
        nonlocal distinct
        freq[arr[i]] = freq.get(arr[i], 0) + 1
        if freq[arr[i]] == 1:
            distinct += 1

    def remove(i):
        nonlocal distinct
        freq[arr[i]] -= 1
        if freq[arr[i]] == 0:
            distinct -= 1

    for i in order:
        ql, qr = queries[i]
        while l > ql:
            l -= 1
            add(l)
        while r < qr:
            r += 1
            add(r)
        while l < ql:
            remove(l)
            l += 1
        while r > qr:
            remove(r)
            r -= 1
        answers[i] = distinct
    return answers

arr = [1, 2, 1, 3, 2, 4, 1]
queries = [(0, 3), (1, 5), (2, 6), (0, 6)]
print(distinct_in_ranges(arr, queries))  # [3, 4, 4, 4] distinct counts

# Hilbert order Mo's matters when you have thousands of range queries
# and no fast update structure fits: frequency queries, distinct counts,
# and range mode problems in competitive programming.
