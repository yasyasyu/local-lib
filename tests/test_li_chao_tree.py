"""li_chao_tree.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from li_chao_tree import LiChaoTree


class TestLiChaoTree(unittest.TestCase):
    def test_single_line(self):
        lct = LiChaoTree(range(10))
        lct.add_line(2, 3)
        for x in range(10):
            self.assertEqual(lct.query(x), 2 * x + 3)

    def test_two_lines_picks_minimum(self):
        xs = list(range(-5, 6))
        lct = LiChaoTree(xs)
        lct.add_line(1, 0)
        lct.add_line(-1, 10)
        for x in xs:
            self.assertEqual(lct.query(x), min(x, -x + 10))

    def test_matches_brute_force_randomized(self):
        random.seed(0)
        xs = list(range(-20, 21))
        for _ in range(10):
            lct = LiChaoTree(xs)
            lines = []
            for _ in range(15):
                a = random.randint(-10, 10)
                b = random.randint(-100, 100)
                lct.add_line(a, b)
                lines.append((a, b))
            for x in xs:
                expected = min(a * x + b for a, b in lines)
                self.assertEqual(lct.query(x), expected, x)

    def test_query_at_duplicate_x_candidates(self):
        lct = LiChaoTree([0, 0, 1, 1, 2])
        lct.add_line(1, 0)
        self.assertEqual(lct.query(2), 2)


if __name__ == "__main__":
    unittest.main()
