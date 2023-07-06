class UnionFind:
    def __init__(self, N) -> None:
        self.p = [-1]*N
        self.r = [-1]*N
    
    def find(self, x):
        if self.p[x] == -1:
            return x
        self.p[x] = self.find(self.p[x])
        return self.p[x]
    
    def merge(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.r[x] > self.r[y]:
            x, y = y, x
        elif self.r[x] == self.r[y]:
            self.r[y] += 1

        self.p[x] = y

    def same(self, x, y):
        return self.find(x) == self.find(y)
