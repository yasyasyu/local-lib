class UnionFind:
    """Union-Find（素集合データ構造）

    使い方:
        uf = UnionFind(5)
        uf.merge(0, 1)
        uf.same(0, 1)   # True
        uf.groups()     # [[0, 1], [2], [3], [4]]

    https://github.com/yasyasyu/local-lib/blob/master/union_find.py
    """

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
            G[self.find(i)].append(i)

        return list(filter(lambda r: r, G))
