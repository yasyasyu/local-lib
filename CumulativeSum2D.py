class CumulativeSum2D:
    def __init__(self, H: int, W: int) -> None:
        self.H = H
        self.W = W
        self.grid = [[0] * (W + 1) for _ in range(H + 1)]

    def add(self, i: int, j: int, v: int = 1) -> None:
        self.grid[(i + 1) * self.W + (j + 1)] += v

    def build(self) -> None:
        for i in range(self.H + 1):
            for j in range(self.W):
                self.grid[i * (self.W + 1) + j + 1] += self.grid[i * (self.W + 1) + j]
        for j in range(self.W + 1):
            for i in range(self.H):
                self.grid[(i + 1) * (self.W + 1) + j] += self.grid[i * (self.W + 1) + j]

    def get(self, i: int, j: int, ii: int, jj: int) -> int:
        return (
            self.grid[ii * (self.W + 1) + jj]
            - self.grid[(i - 1) * (self.W + 1) + jj]
            - self.grid[(ii) * (self.W + 1) + (j - 1)]
            + self.grid[(i - 1) * (self.W + 1) + (j - 1)]
        )
