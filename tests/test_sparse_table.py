"""sparse_table.pyのテストコード"""

import random
import sys
import unittest
from functools import reduce
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sparse_table import SparseTable


class TestSparseTable(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(SparseTable([3, 1, 4, 1, 5, 9, 2, 6]).prod(2, 5), 1)
        self.assertEqual(SparseTable([3, 1, 4, 1, 5], op=max).prod(0, 3), 4)
        self.assertEqual(SparseTable([12, 18, 8], op=gcd).prod(0, 2), 6)

    def test_single_element(self):
        self.assertEqual(SparseTable([7]).prod(0, 1), 7)

    def test_all_ranges_match_brute_force(self):
        rng = random.Random(0)
        for op in (min, max, gcd, lambda x, y: x | y, lambda x, y: x & y):
            for n in list(range(1, 20)) + [64, 65, 100]:
                a = [rng.randint(0, 60) for _ in range(n)]
                st = SparseTable(a, op)
                for l in range(n):
                    for r in range(l + 1, n + 1):
                        self.assertEqual(st.prod(l, r), reduce(op, a[l:r]))

    def test_tuples(self):
        # (値, 添字) で持てば、最小値の位置も分かる
        a = [5, 2, 8, 2, 9]
        st = SparseTable([(v, i) for i, v in enumerate(a)])
        self.assertEqual(st.prod(0, 5), (2, 1))
        self.assertEqual(st.prod(2, 5), (2, 3))


if __name__ == "__main__":
    unittest.main()
