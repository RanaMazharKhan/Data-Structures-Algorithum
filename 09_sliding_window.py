# Sliding window - solve subarray problems in one pass with a fixed moving window

# Idea: instead of checking every subarray from scratch, keep a "window"
# of k items and slide it one step right at a time: add the new element,
# drop the one that falls out. O(n) instead of O(n * k).
# Max sum of any k consecutive numbers:
def max_sum_subarray(nums, k):
    window_sum = sum(nums[:k])      # sum of the first window
    best = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]   # slide: add right, drop left
        if window_sum > best:
            best = window_sum
    return best

print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3))   # 9  (5 + 1 + 3)
print(max_sum_subarray([4, 2, 1, 7, 8, 1, 2, 8, 1, 8], 3))   # 17  (8 + 1 + 8)


# Variable-size window: longest substring with no repeating letters.
# Expand the right edge, and shrink from the left until the repeat is gone.
def longest_unique_substring(s):
    last_seen = {}     # letter -> last index where we saw it
    start = 0          # left edge of the window
    best = ""
    for i, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1   # move window past the repeat
        last_seen[ch] = i
        if len(s[start:i + 1]) > len(best):
            best = s[start:i + 1]
    return len(best), best

print(longest_unique_substring("abcabcbb"))   # (3, 'abc')
print(longest_unique_substring("bbbbb"))      # (1, 'b')


# Why it matters: sliding window is the standard trick for "contiguous"
# problems - log analysis, stock-price windows, network packet streams.
# One pass, constant extra memory, and a favorite interview pattern.
