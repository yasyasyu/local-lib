class UnionFind:
    """Union-Find（素集合データ構造）

    経路圧縮とunion by rankにより、find / merge / sameはならしO(α(N))（実質定数）。

    使い方:
        uf = UnionFind(5)
        uf.merge(0, 1)
        uf.same(0, 1)   # True
        uf.groups()     # [[0, 1], [2], [3], [4]]

    https://github.com/yasyasyu/local-lib/blob/master/union_find.py
    """

    def __init__(self, N) -> None:
        """要素数Nで初期化する。O(N)"""
        self.N = N
        self.parent = [-1] * N
        self.rank = [-1] * N

    def find(self, x):
        """xの属する集合の代表元を返す。ならしO(α(N))"""
        if self.parent[x] == -1:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def merge(self, x, y):
        """xとyの属する集合を併合する。ならしO(α(N))"""
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
        """xとyが同じ集合に属するかを返す。ならしO(α(N))"""
        return self.find(x) == self.find(y)

    def groups(self):
        """集合ごとの要素のリストを返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.find(i)].append(i)

        return list(filter(lambda r: r, G))
