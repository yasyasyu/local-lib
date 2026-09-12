"""cumulative_sum_2d.pyのテストコード

query(i, j, ii, jj) は 1-indexed・両端inclusiveで
行[i, ii]・列[j, jj]の矩形和を返す。
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cumulative_sum_2d import CumulativeSum2D


class TestCumulativeSum2D(unittest.TestCase):
    def test_full_sum(self):
        grid = [[1, 2, 3], [4, 5, 6]]
        cs = CumulativeSum2D(grid)
        self.assertEqual(cs.query(1, 1, 2, 3), sum(sum(row) for row in grid))

    def test_partial_sum(self):
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        cs = CumulativeSum2D(grid)
        # 0-indexed rows[1,2] cols[1,2] -> 1-indexed inclusive (2,2)-(3,3)
        self.assertEqual(cs.query(2, 2, 3, 3), 5 + 6 + 8 + 9)

    def test_single_cell(self):
        grid = [[1, 2], [3, 4]]
        cs = CumulativeSum2D(grid)
        self.assertEqual(cs.query(2, 2, 2, 2), 4)
        self.assertEqual(cs.query(1, 1, 1, 1), 1)

    def test_matches_brute_force(self):
        grid = [[(i * 4 + j + 1) for j in range(4)] for i in range(4)]
        cs = CumulativeSum2D(grid)
        for r0 in range(4):
            for r1 in range(r0, 4):
                for c0 in range(4):
                    for c1 in range(c0, 4):
                        expected = sum(
                            grid[r][c]
                            for r in range(r0, r1 + 1)
                            for c in range(c0, c1 + 1)
                        )
                        got = cs.query(r0 + 1, c0 + 1, r1 + 1, c1 + 1)
                        self.assertEqual(got, expected, (r0, c0, r1, c1))


if __name__ == "__main__":
    unittest.main()
