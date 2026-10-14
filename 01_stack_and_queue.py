# Stack and Queue - two basic data structures every student must know

# A stack is LIFO: last in, first out. Like a pile of plates -
# you take the top one first. push() adds, pop() removes from the top.
class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


# Example: check if brackets are balanced using a stack
# "([])" is balanced, "([)]" is not
def is_balanced(s):
    st = Stack()
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            st.push(ch)
        elif ch in ")]}":
            if st.is_empty() or st.pop() != pairs[ch]:
                return False
    return st.is_empty()


print(is_balanced("([])"))    # True
print(is_balanced("([)]"))    # False
print(is_balanced("{[()]}"))  # True

# ---
# A queue is FIFO: first in, first out. Like a shop line -
# the person who came first is served first.
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, x):
        self.items.append(x)

    def dequeue(self):
        return self.items.pop(0)

    def front(self):
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0


# Example: serve customers in order
q = Queue()
q.enqueue("Ali")
q.enqueue("Sara")
q.enqueue("Ahmed")
print(q.dequeue())  # Ali (came first, served first)
print(q.dequeue())  # Sara
print(q.front())    # Ahmed is next

# ---
# Quick comparison:
# Stack -> undo button, back button in browser, bracket matching
# Queue -> printer jobs, customer service lines, BFS in graphs
