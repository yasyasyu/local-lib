from typing import Any, List


class CumulativeSum2D:
    """2次元累積和

    使い方:
        grid = [[1, 2, 3], [4, 5, 6]]
        cs = CumulativeSum2D(grid)
        cs.query(1, 1, 2, 3)  # 21 (全体の矩形和)

    https://github.com/yasyasyu/local-lib/blob/master/cumulative_sum_2d.py
    """

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
        1-indexed,両端inclusiveで行[i, ii]・列[j, jj]の矩形和を返す。
        """
        i -= 1
        j -= 1
        return (
            self.summed_array[ii][jj]
            - self.summed_array[ii][j]
            - self.summed_array[i][jj]
            + self.summed_array[i][j]
        )
