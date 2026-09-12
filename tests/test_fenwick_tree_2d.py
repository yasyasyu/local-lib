"""fenwick_tree_2d.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fenwick_tree_2d import FenwickTree2D


class TestFenwickTree2D(unittest.TestCase):
    def test_single_point_add_and_sum(self):
        bit = FenwickTree2D(5, 5)
        bit.add(1, 2, 3)
        self.assertEqual(bit.sum(0, 0, 5, 5), 3)
        self.assertEqual(bit.sum(0, 0, 1, 3), 0)
        self.assertEqual(bit.sum(0, 0, 2, 3), 3)

    def test_multiple_points(self):
        bit = FenwickTree2D(5, 5)
        bit.add(1, 2, 3)
        bit.add(3, 3, 4)
        self.assertEqual(bit.sum(0, 0, 5, 5), 7)
        self.assertEqual(bit.sum(0, 0, 2, 3), 3)
        self.assertEqual(bit.sum(2, 2, 5, 5), 4)

    def test_rectangle_excludes_outside_points(self):
        bit = FenwickTree2D(5, 5)
        bit.add(0, 0, 1)
        bit.add(4, 4, 1)
        self.assertEqual(bit.sum(0, 0, 1, 1), 1)
        self.assertEqual(bit.sum(1, 1, 5, 5), 1)

    def test_matches_brute_force_randomized(self):
        random.seed(0)
        h, w = 8, 8
        grid = [[0] * w for _ in range(h)]
        bit = FenwickTree2D(h, w)

        for _ in range(50):
            x, y, val = random.randint(0, h - 1), random.randint(0, w - 1), random.randint(-10, 10)
            grid[x][y] += val
            bit.add(x, y, val)

        for _ in range(50):
            x1 = random.randint(0, h - 1)
            x2 = random.randint(x1 + 1, h)
            y1 = random.randint(0, w - 1)
            y2 = random.randint(y1 + 1, w)
            expected = sum(
                grid[x][y] for x in range(x1, x2) for y in range(y1, y2)
            )
            self.assertEqual(bit.sum(x1, y1, x2, y2), expected, (x1, y1, x2, y2))


if __name__ == "__main__":
    unittest.main()
