# Bit manipulation: using single binary digits as building blocks
# Computers store everything in bits, so a few binary tricks can do
# whole jobs with zero extra memory. & checks a bit, | sets one,
# ^ flips one, << and >> shift digits left or right (like x2 or //2).

# trick 1: count set bits - clear the lowest 1-bit each round
def count_bits(n):
    count = 0
    while n:
        n = n & (n - 1)      # drops the rightmost 1-bit
        count += 1
    return count


# trick 2: is n a power of two? powers of two have exactly one 1-bit
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


# trick 3: the number that appears once while every other appears twice.
# x ^ x = 0 and 0 ^ x = x, so pairs cancel out, leaving the single one.
def single_number(nums):
    answer = 0
    for x in nums:
        answer ^= x
    return answer


# trick 4: swap two numbers with no temp variable
def xor_swap(a, b):
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b


# Example
print(count_bits(13))            # 3 (13 = 1101)
print(is_power_of_two(16))       # True
print(is_power_of_two(18))       # False
print(single_number([4, 1, 2, 1, 2]))  # 4 - everything paired up except 4
print(xor_swap(5, 9))            # (9, 5)

# ---
# Why it matters: these tricks run in O(1) extra space and are a staple
# of interviews and competitive programming. Bitmasks also power sets of
# small items (permissions, chess boards) packed into one integer.
