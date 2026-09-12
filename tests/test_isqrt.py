"""isqrt.pyのテストコード"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from isqrt import isqrt


class TestIsqrt(unittest.TestCase):
    def test_matches_math_isqrt(self):
        for n in [0, 1, 2, 3, 4, 15, 16, 17, 999999, 10**9, 10**18]:
            self.assertEqual(isqrt(n), math.isqrt(n), n)

    def test_perfect_squares(self):
        for k in range(20):
            self.assertEqual(isqrt(k * k), k)


if __name__ == "__main__":
    unittest.main()
