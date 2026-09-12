"""combinatorics.pyのテストコード"""

import sys
import unittest
from math import comb, factorial, perm
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from combinatorics import Combinatorics

MOD = 998244353


class TestCombinatorics(unittest.TestCase):
    def setUp(self):
        self.comb = Combinatorics(30, MOD)

    def test_fact_matches_math_factorial(self):
        for n in range(31):
            self.assertEqual(self.comb.fact(n), factorial(n) % MOD)

    def test_perm_matches_math_perm(self):
        for n in range(10):
            for r in range(n + 1):
                self.assertEqual(self.comb.perm(n, r), perm(n, r) % MOD)

    def test_cmb_matches_math_comb(self):
        for n in range(10):
            for r in range(n + 1):
                self.assertEqual(self.comb.cmb(n, r), comb(n, r) % MOD)

    def test_cmb_out_of_range_is_zero(self):
        self.assertEqual(self.comb.cmb(5, 6), 0)
        self.assertEqual(self.comb.cmb(5, -1), 0)

    def test_perm_out_of_range_is_zero(self):
        self.assertEqual(self.comb.perm(5, 6), 0)

    def test_hcm_matches_stars_and_bars(self):
        for n in range(1, 6):
            for r in range(6):
                self.assertEqual(self.comb.hcm(n, r), comb(n + r - 1, r) % MOD)

    def test_hcm_zero_kinds(self):
        self.assertEqual(self.comb.hcm(0, 0), 1)
        self.assertEqual(self.comb.hcm(0, 3), 0)


if __name__ == "__main__":
    unittest.main()
