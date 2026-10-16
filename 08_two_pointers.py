# Two pointers - solve array problems in one pass without extra memory

# Idea: instead of nested loops, place one pointer at each end (or at two
# different positions) and move them toward each other based on what you see.
# Pair sum on a SORTED list: if the sum is too small, move the left pointer
# right; too big, move the right pointer left.
def pair_sum_sorted(nums, target):
    left = 0
    right = len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return (left, right)
        if total < target:
            left += 1     # sum too small, need a bigger number
        else:
            right -= 1    # sum too big, need a smaller number
    return None

print(pair_sum_sorted([1, 2, 4, 6, 9, 11], 15))   # (2, 5) -> 4 + 11
print(pair_sum_sorted([1, 2, 4, 6, 9, 11], 20))   # (4, 5) -> 9 + 11


# Reverse an array in place: swap the ends, walk both pointers inward.
def reverse_in_place(nums):
    left = 0
    right = len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

nums = [10, 20, 30, 40, 50]
reverse_in_place(nums)
print(nums)   # [50, 40, 30, 20, 10]


# Remove duplicates from a SORTED list: the slow pointer marks the write
# position, the fast pointer scans ahead looking for new values.
def remove_duplicates(nums):
    if len(nums) == 0:
        return []
    write = 0
    for read in range(1, len(nums)):
        if nums[read] != nums[write]:
            write += 1
            nums[write] = nums[read]
    return nums[:write + 1]

print(remove_duplicates([1, 1, 2, 2, 2, 3, 4, 4]))   # [1, 2, 3, 4]


# Why it matters: two pointers turns O(n^2) nested-loop problems into O(n)
# single passes - it is a favorite interview pattern (pair sums, palindromes,
# merging sorted lists) and shows up in string/array problems everywhere.
