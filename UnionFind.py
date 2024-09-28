class UnionFind:
    def __init__(self, N) -> None:
        self.N = N
        self.parent = [-1] * N
        self.rank = [-1] * N

    def find(self, x):
        if self.parent[x] == -1:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def merge(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.rank[x] > self.rank[y]:
            x, y = y, x
        elif self.rank[x] == self.rank[y]:
            self.rank[y] += 1

        self.parent[x] = y

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def groups(self):
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            if root := self.find(i) == -1:
                G[i].append(i)
            else:
                G[root].append(i)

        return list(filter(lambda r: r, G))
