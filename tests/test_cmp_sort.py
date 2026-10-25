"""cmp_sort.pyのテストコード"""

import random
import sys
import unittest
from functools import cmp_to_key
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cmp_sort import sort_by_cmp


def frac_cmp(p, q):
    return p[0] * q[1] - q[0] * p[1]


class TestSortByCmp(unittest.TestCase):
    def test_docstring_fraction(self):
        self.assertEqual(sort_by_cmp([(1, 2), (1, 3), (2, 3)], frac_cmp), [(1, 3), (1, 2), (2, 3)])

    def test_docstring_concat(self):
        cmp = lambda x, y: (x + y > y + x) - (x + y < y + x)
        self.assertEqual(sort_by_cmp(["3", "30", "34"], cmp), ["30", "3", "34"])

    def test_empty_and_single(self):
        self.assertEqual(sort_by_cmp([], frac_cmp), [])
        self.assertEqual(sort_by_cmp([(1, 2)], frac_cmp), [(1, 2)])

    def test_does_not_modify_input(self):
        a = [3, 1, 2]
        sort_by_cmp(a, lambda x, y: x - y)
        self.assertEqual(a, [3, 1, 2])

    def test_descending(self):
        self.assertEqual(sort_by_cmp([3, 1, 4, 1, 5], lambda x, y: y - x), [5, 4, 3, 1, 1])

    def test_stable(self):
        # 1/2 と 2/4 は等しいので、元の順番が保たれる
        a = [(2, 4), (1, 3), (1, 2), (3, 6)]
        self.assertEqual(sort_by_cmp(a, frac_cmp), [(1, 3), (2, 4), (1, 2), (3, 6)])

    def test_random_matches_cmp_to_key(self):
        rng = random.Random(0)
        for n in list(range(20)) + [100, 1000]:
            a = [(rng.randint(1, 10), rng.randint(1, 10)) for _ in range(n)]
            self.assertEqual(sort_by_cmp(a, frac_cmp), sorted(a, key=cmp_to_key(frac_cmp)))


if __name__ == "__main__":
    unittest.main()
