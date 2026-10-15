# Linear search vs binary search - finding an item in a list

# Linear search checks every element one by one until it finds the target.
# Simple, works on any list (sorted or not), but slow on big data: O(n).
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i   # found at index i
    return -1          # not found


# Binary search works only on SORTED lists. It looks at the middle element:
# if the target is smaller, search the left half; if bigger, the right half.
# Each step throws away half the list, so it is very fast: O(log n).
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid        # found at index mid
        elif arr[mid] < target:
            low = mid + 1     # target is in the right half
        else:
            high = mid - 1    # target is in the left half
    return -1                 # not found


# Small example: both find the target at index 4
nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(linear_search(nums, 16))  # 4
print(binary_search(nums, 16))  # 4
print(binary_search(nums, 99))   # -1 (not in the list)

# ---
# Timing comparison on a big sorted list of 1,000,000 numbers.
# linear_search would need up to 1,000,000 checks;
# binary_search needs only ~20 checks (2^20 > 1,000,000).
import time
big = list(range(1000000))
target = 999999

start = time.time()
linear_search(big, target)
print("linear search time:", round(time.time() - start, 4), "seconds")

start = time.time()
binary_search(big, target)
print("binary search time:", round(time.time() - start, 6), "seconds")

# ---
# Why it matters: search is everywhere - finding a name in contacts,
# a word in a dictionary, a row in a database. Whenever data is sorted,
# binary search (or indexes built on the same idea) makes it instant.
