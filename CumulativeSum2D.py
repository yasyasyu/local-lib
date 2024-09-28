from typing import Any, List


class CumulativeSum2D:
    def __init__(self, array: List[List[Any]]) -> None:
        self.height: int = len(array)
        self.width: int = len(array[0])
        self.summed_array: List[List[Any]] = [
            [0] * (self.width + 1) for _ in range(self.height + 1)
        ]
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                self.summed_array[i][j] = array[i - 1][j - 1]

        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                self.summed_array[i][j] += (
                    self.summed_array[i][j - 1]
                    + self.summed_array[i - 1][j]
                    - self.summed_array[i - 1][j - 1]
                )

    def query(self, i: int, j: int, ii: int, jj: int) -> int:
        """
        sum ((i:ii] (j:jj])
        """
        i -= 1
        j -= 1
        return (
            self.summed_array[ii][jj]
            - self.summed_array[ii][j]
            - self.summed_array[i][jj]
            + self.summed_array[i][j]
        )
