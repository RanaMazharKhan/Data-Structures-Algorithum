# Practice set 4: mixed problems from everything covered so far
# Each problem is a one-paragraph comment plus a short solution.
# Try to solve it yourself before reading the code below it.

# problem 1 (hash table): first non-repeating character in a string.
# A count map does it in one pass; then scan the string for count 1.
def first_unique_char(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


# problem 2 (two pointers): move all zeros to the end, keeping order.
# The 'write' pointer marks the next slot for a non-zero number.
def move_zeros(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    return nums


# problem 3 (sliding window + hash map): longest substring with at most
# k distinct characters. Grow the right edge, shrink from the left while
# the window has too many distinct letters.
def longest_k_distinct(s, k):
    counts, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


# problem 4 (binary search on answer): smallest ship capacity that
# delivers all packages within 'days'. Capacity too small -> more days.
def ship_within_days(weights, days):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        needed, load = 1, 0
        for w in weights:
            if load + w > mid:
                needed += 1
                load = 0
            load += w
        if needed <= days:
            hi = mid       # this capacity works, try smaller
        else:
            lo = mid + 1   # need a bigger ship
    return lo


# run the checks
print(first_unique_char("leetcode"))          # 0 ('l' is the first unique)
print(move_zeros([0, 1, 0, 3, 12]))           # [1, 3, 12, 0, 0]
print(longest_k_distinct("eceba", 2))         # 3 ("ece")
print(ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))  # 15

# ---
# Why it matters: interviews rarely ask one pure topic - they mix hash
# maps with windows, pointers with binary search. Practicing the combos
# is what turns knowledge of data structures into problem-solving speed.
