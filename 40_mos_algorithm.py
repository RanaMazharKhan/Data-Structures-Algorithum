# Mo's algorithm: answering offline range queries by reordering

# A range query asks something about arr[l:r], like how many distinct
# numbers are inside it. Answering each query from scratch is O(n).
# Mo's trick: sort all the queries first, then slide one window around
# instead of starting over for every query.

# Sort queries into blocks of size sqrt(n) by their left end, and
# inside a block sort by right end. Queries that are close together
# then share most of their window, so moving between them is cheap.
# Adding a number updates a frequency table, removing one undoes it,
# so the window can slide left or right one step at a time.

def mos_distinct(arr, queries):
    n = len(arr)
    block = int(n ** 0.5) or 1
    # keep each query's original position so answers go back in order
    order = sorted(range(len(queries)), key=lambda i: (
        queries[i][0] // block,
        queries[i][1] if (queries[i][0] // block) % 2 == 0 else -queries[i][1]))
    freq = {}
    distinct = 0
    answers = [0] * len(queries)
    left = right = 0  # current window is arr[left:right], empty at start

    def add(x):
        nonlocal distinct
        freq[x] = freq.get(x, 0) + 1
        if freq[x] == 1:
            distinct += 1

    def remove(x):
        nonlocal distinct
        freq[x] -= 1
        if freq[x] == 0:
            distinct -= 1

    for i in order:
        l, r = queries[i]  # query asks about arr[l:r], r not included
        while left > l:
            left -= 1
            add(arr[left])
        while right < r:
            add(arr[right])
            right += 1
        while left < l:
            remove(arr[left])
            left += 1
        while right > r:
            right -= 1
            remove(arr[right])
        answers[i] = distinct
    return answers


arr = [1, 2, 1, 3, 2, 4, 1]
queries = [(0, 4), (1, 6), (2, 7), (0, 7)]
print(mos_distinct(arr, queries))  # [3, 4, 4, 4]

# ---
# Why it matters: Mo's algorithm turns many slow range queries into one
# fast sweep, which is why it is a favourite in competitive programming
# whenever queries are known in advance (offline) and the array is static.
