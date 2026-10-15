# Singly linked list - a chain of nodes where each node points to the next

# A node is just a box holding data and a link (pointer) to the next box.
# Unlike a list, nodes are not stored in one block of memory -
# they are linked together, so inserting/deleting in the middle is easy.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# The linked list class manages the chain. It keeps track of the head
# (first node), and provides insert, delete, traverse and reverse.
class LinkedList:
    def __init__(self):
        self.head = None

    # Insert a new node at the end of the list
    def append(self, data):
        new_node = Node(data)
        if self.head is None:      # empty list -> new node becomes head
            self.head = new_node
            return
        curr = self.head
        while curr.next is not None:   # walk to the last node
            curr = curr.next
        curr.next = new_node

    # Insert a new node at the front (position 0)
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head  # old head becomes the second node
        self.head = new_node       # new node is now the head

    # Delete the first node whose data equals key
    def delete(self, key):
        curr = self.head
        prev = None
        while curr is not None:
            if curr.data == key:
                if prev is None:          # deleting the head
                    self.head = curr.next
                else:                     # bypass the node: it is removed from the chain
                    prev.next = curr.next
                return True
            prev = curr
            curr = curr.next
        return False   # key not found

    # Traverse: walk node by node and print the data
    def print_list(self):
        curr = self.head
        while curr is not None:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")

    # Reverse the list in place by flipping the links
    def reverse(self):
        prev = None
        curr = self.head
        while curr is not None:
            nxt = curr.next    # save the next node
            curr.next = prev   # flip this node's link
            prev = curr        # move prev and curr one step forward
            curr = nxt
        self.head = prev       # prev is the new head


# Example: build the list 10 -> 20 -> 30, then modify it
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.print_list()        # 10 -> 20 -> 30 -> None

ll.prepend(5)          # insert at front
ll.print_list()        # 5 -> 10 -> 20 -> 30 -> None

ll.delete(20)          # delete a node in the middle
ll.print_list()        # 5 -> 10 -> 30 -> None

ll.reverse()           # flip all links
ll.print_list()        # 30 -> 10 -> 5 -> None

# ---
# Why it matters: linked lists are the foundation of many other structures
# (stacks, queues, hash-table chaining, adjacency lists for graphs).
# Real uses: browser history (back/forward), music playlists, undo systems.
