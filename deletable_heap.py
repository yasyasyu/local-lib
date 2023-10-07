import heapq

class DeletableHeap:
    def __init__(self, is_unique = False):
        self.heap = []
        self.d = dict()
        self.size = 0
        self.total = 0
        self.is_unique = is_unique

    def __str__(self):
        return f"[{', '.join(map(str, self.heap))}]"

    def push(self, x):
        if x not in self.d:
            self.d[x] = 1
        elif self.is_unique:
            return
        else:
            self.d[x] += 1

        self.size += 1
        self.total += x
        heapq.heappush(self.heap, x)


    def get(self):
        return self.heap[0]

    def pop(self):
        n = self.get()
        self.discard(n)
        return n

    def discard(self, x):
        if not self.is_exist(x):
            return False

        self.size -= 1
        self.total -= x
        self.d[x] -= 1
        if self.d[x] == 0:
            del self.d[x]

        while len(self.heap) != 0 and self.heap[0] not in self.d:
            heapq.heappop(self.heap)
        return True

    def erase(self, x, n=10**18):
        if not self.is_exist(x):
            return 0

        if self.d[x] < n:
            n = self.d[x]
        self.size -= n
        self.total -= x * n
        self.d[x] -= n
        if self.d[x] == 0:
            del self.d[x]

        while len(self.heap) != 0 and self.heap[0] not in self.d:
            heapq.heappop(self.heap)
        return n

    def is_exist(self, x):
        return x in self.d

    def __len__(self):
        return self.size

    def types(self):
        return len(self.d)

    def sum(self):
        return self.total

    def count(self, x):
        return self.d[x] if self.is_exist(x) else 0
