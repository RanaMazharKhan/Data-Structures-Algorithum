# Heap / priority queue with heapq: always get the smallest (or largest) item fast

# A heap is a binary tree stored in a list where the smallest item is
# always at index 0. Pushing and popping both take O(log n) time.
# heapq makes a MIN-heap: the smallest number comes out first.
import heapq

tasks = []
# Each entry is (priority, name). Lower priority number = more urgent.
heapq.heappush(tasks, (3, "reply to email"))
heapq.heappush(tasks, (1, "fix server outage"))
heapq.heappush(tasks, (2, "submit report"))
print(heapq.heappop(tasks))  # (1, 'fix server outage') - most urgent first
print(heapq.heappop(tasks))  # (2, 'submit report')
print(tasks)                 # [(3, 'reply to email')]

# MAX-heap trick: store negative numbers, so the biggest original
# value becomes the smallest negative and pops first.
scores = []
for s in [85, 97, 72, 91]:
    heapq.heappush(scores, -s)
print(-heapq.heappop(scores))  # 97
print(-heapq.heappop(scores))  # 91

# Classic use: top-k elements. Heapify the list (O(n)), then pop k times.
def top_k(nums, k):
    heap = nums[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(k)]

print(top_k([40, 10, 30, 20, 50], 3))  # [10, 20, 30]

# A min-heap can also merge two sorted lists cheaply.
print(list(heapq.merge([1, 3, 5], [2, 4, 6])))  # [1, 2, 3, 4, 5, 6]

# Heaps matter because "give me the most important thing next" shows up
# everywhere: task schedulers, shortest-path algorithms (Dijkstra),
# leaderboards, and finding the top-k of millions of items without
# sorting the whole thing.
