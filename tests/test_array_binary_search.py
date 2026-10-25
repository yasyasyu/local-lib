"""array_binary_search.pyのテストコード"""

import bisect
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from array_binary_search import lower_bound, partition_point, upper_bound

desc = lambda x, y: y - x


class TestLowerUpperBound(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(lower_bound([1, 3, 3, 5], 3), 1)
        self.assertEqual(lower_bound([1, 3, 3, 5], 4), 3)
        self.assertEqual(lower_bound([5, 3, 3, 1], 3, desc), 1)
        self.assertEqual(upper_bound([1, 3, 3, 5], 3), 3)
        self.assertEqual(upper_bound([1, 3, 3, 5], 0), 0)

    def test_empty(self):
        self.assertEqual(lower_bound([], 1), 0)
        self.assertEqual(upper_bound([], 1, desc), 0)

    def test_not_found_returns_hi(self):
        self.assertEqual(lower_bound([1, 2, 3], 9), 3)
        self.assertEqual(upper_bound([3, 2, 1], 0, desc), 3)

    def test_cmp_matches_bisect(self):
        rng = random.Random(0)
        asc = lambda x, y: x - y
        for _ in range(300):
            a = sorted(rng.randint(0, 10) for _ in range(rng.randint(0, 15)))
            x = rng.randint(-1, 11)
            self.assertEqual(lower_bound(a, x, asc), bisect.bisect_left(a, x))
            self.assertEqual(upper_bound(a, x, asc), bisect.bisect_right(a, x))

    def test_descending_count(self):
        rng = random.Random(1)
        for _ in range(300):
            a = sorted((rng.randint(0, 10) for _ in range(rng.randint(0, 15))), reverse=True)
            x = rng.randint(-1, 11)
            lb = lower_bound(a, x, desc)
            ub = upper_bound(a, x, desc)
            self.assertTrue(all(v > x for v in a[:lb]))
            self.assertTrue(all(v < x for v in a[ub:]))
            self.assertEqual(ub - lb, a.count(x))

    def test_lo_hi(self):
        a = [1, 3, 3, 5, 7, 9]
        self.assertEqual(lower_bound(a, 3, lo=2), 2)
        self.assertEqual(lower_bound(a, 9, hi=4), 4)
        self.assertEqual(upper_bound(a, 3, lambda x, y: x - y, lo=4), 4)
        self.assertEqual(upper_bound(a, 9, lambda x, y: x - y, hi=4), 4)


class TestPartitionPoint(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(partition_point([1, 3, 3, 5, 8], lambda v: v * v < 20), 3)
        b = [(0, 1), (0, 4), (1, 2), (1, 9)]
        self.assertEqual(partition_point(b, lambda p: p[0] < 1), 2)

    def test_all_true_and_all_false(self):
        a = [1, 2, 3]
        self.assertEqual(partition_point(a, lambda v: True), 3)
        self.assertEqual(partition_point(a, lambda v: False), 0)
        self.assertEqual(partition_point([], lambda v: True), 0)

    def test_lo_hi(self):
        a = [1, 2, 3, 4, 5]
        self.assertEqual(partition_point(a, lambda v: v < 4, lo=1, hi=3), 3)
        self.assertEqual(partition_point(a, lambda v: v < 2, lo=2), 2)

    def test_random_matches_linear(self):
        rng = random.Random(2)
        for _ in range(300):
            a = sorted(rng.randint(0, 10) for _ in range(rng.randint(0, 15)))
            t = rng.randint(-1, 11)
            expected = sum(1 for v in a if v < t)
            self.assertEqual(partition_point(a, lambda v: v < t), expected)


if __name__ == "__main__":
    unittest.main()
