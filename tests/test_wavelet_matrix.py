"""wavelet_matrix.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from wavelet_matrix import WaveletMatrix


class TestWaveletMatrix(unittest.TestCase):
    def test_docstring_examples(self):
        wm = WaveletMatrix([5, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(wm.kth_smallest(1, 6, 0), 1)
        self.assertEqual(wm.kth_smallest(1, 6, 2), 4)
        self.assertEqual(wm.kth_largest(1, 6, 0), 9)
        self.assertEqual(wm.range_freq(0, 8, 2, 6), 4)
        self.assertEqual(wm.count(0, 8, 5), 2)
        self.assertEqual(wm.prev_value(0, 8, 5), 4)
        self.assertEqual(wm.next_value(0, 8, 7), 9)

    def test_empty_and_single_value(self):
        wm = WaveletMatrix([])
        self.assertEqual(wm.range_freq(0, 0, 0, 10), 0)
        self.assertIsNone(wm.prev_value(0, 0, 10))
        wm = WaveletMatrix([7, 7, 7])
        self.assertEqual(wm.kth_smallest(0, 3, 2), 7)
        self.assertEqual(wm.count(0, 3, 7), 3)
        self.assertEqual(wm.access(1), 7)

    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(100):
            n = rng.randint(1, 25)
            a = [rng.randint(-10, 10) for _ in range(n)]
            wm = WaveletMatrix(a)
            self.assertEqual([wm.access(i) for i in range(n)], a)
            for _ in range(50):
                l = rng.randrange(n)
                r = rng.randint(l + 1, n)
                sub = sorted(a[l:r])
                k = rng.randrange(r - l)
                self.assertEqual(wm.kth_smallest(l, r, k), sub[k])
                self.assertEqual(wm.kth_largest(l, r, k), sub[::-1][k])
                lo, hi = rng.randint(-12, 12), rng.randint(-12, 12)
                self.assertEqual(wm.range_freq(l, r, lo, hi), sum(1 for x in sub if lo <= x < hi))
                x = rng.randint(-12, 12)
                self.assertEqual(wm.count(l, r, x), sub.count(x))
                below = [y for y in sub if y < x]
                above = [y for y in sub if y >= x]
                self.assertEqual(wm.prev_value(l, r, x), max(below) if below else None)
                self.assertEqual(wm.next_value(l, r, x), min(above) if above else None)

    def test_large_values(self):
        a = [10**18, -(10**18), 0, 10**18]
        wm = WaveletMatrix(a)
        self.assertEqual(wm.kth_smallest(0, 4, 3), 10**18)
        self.assertEqual(wm.range_freq(0, 4, 0, 10**18 + 1), 3)


if __name__ == "__main__":
    unittest.main()
