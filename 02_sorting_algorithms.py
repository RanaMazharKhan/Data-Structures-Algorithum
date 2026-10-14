# Sorting algorithms - the first algorithms every student learns
# We sort the same list with each one and compare.

data = [64, 25, 12, 22, 11]

# Bubble sort: compare neighbours and swap if wrong order.
# Biggest value "bubbles" to the end each pass. O(n^2).
def bubble_sort(a):
    a = a[:]  # work on a copy
    n = len(a)
    for i in range(n):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


# Insertion sort: build the sorted list one item at a time,
# inserting each new item in its correct place. O(n^2) but
# fast on small or nearly-sorted lists.
def insertion_sort(a):
    a = a[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# Merge sort: divide and conquer. Split the list in half,
# sort each half, then merge. O(n log n) - much faster on big lists.
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


print("original: ", data)
print("bubble:   ", bubble_sort(data))
print("insertion:", insertion_sort(data))
print("merge:    ", merge_sort(data))

# ---
# When to use what:
# bubble/insertion -> only for learning or tiny lists (O(n^2) is slow)
# merge sort       -> good default, O(n log n), needs extra memory
# Python's sorted() uses Timsort (merge + insertion hybrid) - fastest in practice
import time
big = list(range(2000, 0, -1))
t = time.time(); merge_sort(big); print("merge 2000 items: %.4fs" % (time.time() - t))
t = time.time(); bubble_sort(big); print("bubble 2000 items: %.4fs" % (time.time() - t))
