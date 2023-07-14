class doubling:
    def __init__(self, ne, K):
        self.n = len(ne)
        self.ne = ne
        self.K = K
        self.D = [[0] * self.n for _ in range(K + 1)]
        for i in range(self.n):
            self.D[0][i] = ne[i]
        for k in range(K):
            d = self.D[k]
            nd = self.D[k + 1]
            for i in range(self.n):
                a = d[i]
                if 0 <= a < self.n:
                    nd[i] = d[a]
                else:
                    nd[i] = a

    def query(self, i, t):
        s = i
        for k in range(self.K):
            if t & 1:
                i = self.D[k][i]
                if not 0 <= i < self.n:
                    return i
            t >>= 1
        return i
