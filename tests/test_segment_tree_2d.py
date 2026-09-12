"""segment_tree_2d.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from segment_tree_2d import SegmentTree2D

INF = float("inf")


class TestSegmentTree2D(unittest.TestCase):
    def test_basic_min_query(self):
        seg = SegmentTree2D(3, 3, op=min, e=INF)
        seg.update(1, 1, 5)
        seg.update(0, 2, 3)
        self.assertEqual(seg.query(0, 0, 3, 3), 3)
        self.assertEqual(seg.query(0, 0, 2, 2), 5)
        self.assertEqual(seg.get(1, 1), 5)
        self.assertEqual(seg.get(0, 0), INF)

    def test_query_excludes_outside_rectangle(self):
        seg = SegmentTree2D(4, 4, op=lambda a, b: a + b, e=0)
        seg.update(0, 0, 1)
        seg.update(3, 3, 100)
        self.assertEqual(seg.query(0, 0, 1, 1), 1)
        self.assertEqual(seg.query(1, 1, 4, 4), 100)
        self.assertEqual(seg.query(0, 0, 4, 4), 101)

    def test_update_overwrites_previous_value(self):
        seg = SegmentTree2D(2, 2, op=max, e=-INF)
        seg.update(0, 0, 5)
        seg.update(0, 0, 3)
        self.assertEqual(seg.get(0, 0), 3)
        self.assertEqual(seg.query(0, 0, 2, 2), 3)

    def test_build_from_initial_grid(self):
        v = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        seg = SegmentTree2D(3, 3, op=lambda a, b: a + b, e=0, v=v)
        self.assertEqual(seg.query(0, 0, 3, 3), 45)
        self.assertEqual(seg.query(0, 0, 2, 2), 1 + 2 + 4 + 5)
        self.assertEqual(seg.get(2, 2), 9)

    def test_non_square_grid(self):
        v = [[1, 2, 3, 4], [5, 6, 7, 8]]
        seg = SegmentTree2D(2, 4, op=max, e=-INF, v=v)
        self.assertEqual(seg.query(0, 0, 2, 4), 8)
        self.assertEqual(seg.query(0, 0, 1, 4), 4)
        self.assertEqual(seg.query(1, 2, 2, 4), 8)

    def test_matches_brute_force_randomized_sum(self):
        random.seed(0)
        h, w = 7, 6
        grid = [[0] * w for _ in range(h)]
        seg = SegmentTree2D(h, w, op=lambda a, b: a + b, e=0)

        for _ in range(80):
            if random.random() < 0.7:
                x, y, val = (
                    random.randint(0, h - 1),
                    random.randint(0, w - 1),
                    random.randint(-20, 20),
                )
                grid[x][y] = val
                seg.update(x, y, val)
            else:
                x1 = random.randint(0, h - 1)
                x2 = random.randint(x1 + 1, h)
                y1 = random.randint(0, w - 1)
                y2 = random.randint(y1 + 1, w)
                expected = sum(
                    grid[x][y] for x in range(x1, x2) for y in range(y1, y2)
                )
                self.assertEqual(seg.query(x1, y1, x2, y2), expected, (x1, y1, x2, y2))

    def test_matches_brute_force_randomized_min(self):
        random.seed(1)
        h, w = 6, 5
        grid = [[INF] * w for _ in range(h)]
        seg = SegmentTree2D(h, w, op=min, e=INF)

        for _ in range(80):
            if random.random() < 0.7:
                x, y, val = (
                    random.randint(0, h - 1),
                    random.randint(0, w - 1),
                    random.randint(-20, 20),
                )
                grid[x][y] = val
                seg.update(x, y, val)
            else:
                x1 = random.randint(0, h - 1)
                x2 = random.randint(x1 + 1, h)
                y1 = random.randint(0, w - 1)
                y2 = random.randint(y1 + 1, w)
                expected = min(
                    grid[x][y] for x in range(x1, x2) for y in range(y1, y2)
                )
                self.assertEqual(seg.query(x1, y1, x2, y2), expected, (x1, y1, x2, y2))


if __name__ == "__main__":
    unittest.main()
