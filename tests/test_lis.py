"""lis.pyのテストコード"""

import itertools
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lis import lis, lis_ending_at


def is_increasing(vals, strict):
    return all((x < y) if strict else (x <= y) for x, y in zip(vals, vals[1:]))


def brute_ending_at(a, strict):
    n = len(a)
    res = [1] * n
    for i in range(n):
        for j in range(i):
            if (a[j] < a[i]) if strict else (a[j] <= a[i]):
                res[i] = max(res[i], res[j] + 1)
    return res


def brute_lis_len(a, strict):
    best = 0
    for r in range(len(a) + 1):
        for idx in itertools.combinations(range(len(a)), r):
            if is_increasing([a[i] for i in idx], strict):
                best = max(best, r)
    return best


class TestLis(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(lis_ending_at([3, 1, 4, 1, 5, 9, 2, 6]), [1, 1, 2, 1, 3, 4, 2, 4])
        self.assertEqual(lis_ending_at([1, 1, 2], strict=False), [1, 2, 3])
        self.assertEqual(lis([3, 1, 4, 1, 5, 9, 2, 6]), [1, 2, 4, 7])

    def test_empty(self):
        self.assertEqual(lis_ending_at([]), [])
        self.assertEqual(lis([]), [])

    def test_through_example(self):
        a = [3, 1, 4, 1, 5, 9, 2, 6]
        left = lis_ending_at(a)
        right = lis_ending_at([-x for x in reversed(a)])[::-1]
        through = [l + r - 1 for l, r in zip(left, right)]
        for i in range(len(a)):
            # a[i] を必ず通る最長増加部分列の長さを全探索で求める
            best = 0
            for r in range(1, len(a) + 1):
                for idx in itertools.combinations(range(len(a)), r):
                    if i in idx and is_increasing([a[j] for j in idx], True):
                        best = max(best, r)
            self.assertEqual(through[i], best)

    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(300):
            a = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
            for strict in (True, False):
                self.assertEqual(lis_ending_at(a, strict), brute_ending_at(a, strict))
                idx = lis(a, strict)
                self.assertEqual(idx, sorted(idx))
                self.assertTrue(is_increasing([a[i] for i in idx], strict))
                self.assertEqual(len(idx), brute_lis_len(a, strict))

    def test_strings(self):
        self.assertEqual(len(lis(list("abcabd"))), 4)  # a, b, c, d


if __name__ == "__main__":
    unittest.main()
