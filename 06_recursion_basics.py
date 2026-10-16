# Recursion basics - a function that calls itself until a base case stops it

# factorial: n! = n * (n-1) * ... * 1.
# The base case (n <= 1) stops the recursion, otherwise the function
# calls itself with a smaller n and waits for the answer to come back.
def factorial(n):
    if n <= 1:
        return 1              # base case: 1! = 1, 0! = 1
    return n * factorial(n - 1)   # recursive case: n * (n-1)!

print(factorial(5))   # 120
print(factorial(0))   # 1


# fibonacci: each number is the sum of the two before it.
# Same idea: base cases stop it, each call splits into two smaller calls.
def fibonacci(n):
    if n == 0:
        return 0              # base case
    if n == 1:
        return 1              # base case
    return fibonacci(n - 1) + fibonacci(n - 2)

print([fibonacci(i) for i in range(10)])   # 0 1 1 2 3 5 8 13 21 34


# Call stack idea: every recursive call waits on a "stack" until the
# calls inside it finish. A print before the call shows the calls going
# down, a print after shows them coming back up.
def countdown(n):
    print("going down:", n)
    if n == 0:
        return                # base case stops the stack from growing
    countdown(n - 1)
    print("coming back up:", n)

countdown(3)


# A classic: sum of a list without any loop, pure recursion.
def list_sum(nums):
    if len(nums) == 0:
        return 0              # base case: empty list sums to 0
    return nums[0] + list_sum(nums[1:])

print(list_sum([4, 5, 6, 7]))   # 22


# Why it matters: recursion powers tree/graph traversals, sorting
# (merge sort, quick sort) and divide-and-conquer solutions.
# Mastering the base case vs recursive case pattern makes those
# advanced topics click instead of feeling like magic.
