class PotentialUnionFind:
    def __init__(self, N, inf=10**18):
        self.N = N
        self.parent = [-1] * N
        self.potential = [0] * N
        self.INF = inf

    def root(self, a):
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
        ra = self.root(a)
        rb = self.root(b)
        if ra == rb:
            return self.potential[b] - self.potential[a]
        return self.INF

    def unite(self, a, b, d):
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
        return -self.parent[self.root(a)]

    def groups(self):
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        return [g for g in G if g]

    def groups_index(self):
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
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        return [len(g) for g in G if g]
