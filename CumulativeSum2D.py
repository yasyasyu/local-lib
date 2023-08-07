class CumulativeSum2D:
    def __init__(self, H: int, W: int) -> None:
        self.H = H
        self.W = W
        self.H1 = H + 1
        self.W1 = W + 1
        self.arr = [0] * (self.W * self.H)
        self.carr = [0] * (self.H1 * self.W1)

    def add(self, i: int, j: int, v: int = 1) -> None:
        self.arr[i * self.W + j] += v

    def build(self) -> None:
        for i in range(self.H):
            for j in range(self.W):
                self.carr[(i + 1) * self.W1 + (j + 1)] = (
                    self.carr[(i) * self.W1 + (j + 1)]
                    + self.carr[(i + 1) * self.W1 + (j)]
                    - self.carr[(i) * self.W1 + (j)]
                    + self.arr[(i) * self.W + (j)]
                )

    def get(self, i: int, j: int, ii: int, jj: int) -> int:
        return (
            self.carr[ii * self.W1 + jj]
            - self.carr[ii * self.W1 + j]
            - self.carr[i * self.W1 + jj]
            + self.carr[i * self.W1 + j]
        )
