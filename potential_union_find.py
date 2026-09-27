class PotentialUnionFind:
    """重み付きUnion-Find（ポテンシャル付き素集合データ構造）

    unite(a, b, d) で「potential[b] - potential[a] = d」という関係を追加する。
    連結判定は same() ではなく dist(a, b) != INF で行う。

    経路圧縮とunion by sizeにより、root / dist / unite / sizeはならしO(α(N))（実質定数）。

    使い方:
        uf = PotentialUnionFind(3)
        uf.unite(0, 1, 5)  # potential[1] - potential[0] = 5
        uf.dist(0, 1)      # 5
        uf.dist(1, 2)      # 未連結ならINF

    https://github.com/yasyasyu/local-lib/blob/master/potential_union_find.py
    """

    def __init__(self, N, inf=10**18):
        """要素数Nで初期化する。O(N)"""
        self.N = N
        self.parent = [-1] * N
        self.potential = [0] * N
        self.INF = inf

    def root(self, a):
        """aの属する集合の根を返す（経路圧縮しつつポテンシャルを更新する）。ならしO(α(N))"""
        a0 = a
        s = 0
        L1 = []
        while self.parent[a] >= 0:
            L1.append((a, self.potential[a]))
            s += self.potential[a]
            a = self.parent[a]
        pa = a
        a = a0
        L2 = []
        while a != pa:
            L2.append((a, self.potential[a]))
            self.potential[a], s = s, s - self.potential[a]
            self.parent[a], a = pa, self.parent[a]
        return pa

    def dist(self, a, b):
        """potential[b] - potential[a]を返す。未連結ならINF。ならしO(α(N))"""
        ra = self.root(a)
        rb = self.root(b)
        if ra == rb:
            return self.potential[b] - self.potential[a]
        return self.INF

    def unite(self, a, b, d):
        """potential[b] - potential[a] = dという関係を追加する。ならしO(α(N))"""
        ra, rb = self.root(a), self.root(b)
        if ra != rb:
            if self.parent[rb] >= self.parent[ra]:
                self.parent[ra] += self.parent[rb]
                self.potential[rb] = self.potential[a] + d - self.potential[b]
                self.parent[rb] = ra
            else:
                self.parent[rb] += self.parent[ra]
                self.potential[ra] = self.potential[b] - d - self.potential[a]
                self.parent[ra] = rb

    def size(self, a):
        """aの属する集合の要素数を返す。ならしO(α(N))"""
        return -self.parent[self.root(a)]

    def groups(self):
        """集合ごとの要素のリストを返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        return [g for g in G if g]

    def groups_index(self):
        """集合ごとの要素のリストと、根から集合の番号への対応を返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        cnt = 0
        GG = []
        I = [-1] * self.N
        for i in range(self.N):
            if G[i]:
                GG.append(G[i])
                I[i] = cnt
                cnt += 1
        return GG, I

    def group_size(self):
        """各集合の要素数のリストを返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        return [len(g) for g in G if g]
