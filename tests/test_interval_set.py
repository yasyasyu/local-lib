"""interval_set.pyのテストコード

interval_set.pyは `from .sorted_multi_set import SortedMultiset` という
相対インポートを使っているため、パッケージとしてインポートする必要がある。
親ディレクトリをsys.pathに追加し、フォルダ名前空間パッケージ経由で読み込む。
"""

import importlib
import random
import sys
import unittest
from pathlib import Path

_LIB_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_LIB_DIR.parent))

IntervalSet = importlib.import_module(f"{_LIB_DIR.name}.interval_set").IntervalSet


class TestIntervalSet(unittest.TestCase):
    def test_add_and_contains(self):
        s = IntervalSet()
        self.assertTrue(s.add(5))
        self.assertFalse(s.add(5))
        self.assertTrue(s.contains(5))
        self.assertFalse(s.contains(6))
        self.assertEqual(len(s), 1)

    def test_add_merges_adjacent_intervals(self):
        s = IntervalSet()
        s.add(1)
        s.add(3)
        s.add(2)
        self.assertEqual(str(s), "[(1, 4)]")
        self.assertEqual(len(s), 3)

    def test_insert_interval(self):
        s = IntervalSet()
        s.insert(1, 5)  # [1,5)
        self.assertEqual(len(s), 4)
        for x in [1, 2, 3, 4]:
            self.assertTrue(s.contains(x))
        self.assertFalse(s.contains(5))

    def test_remove(self):
        s = IntervalSet()
        s.insert(0, 5)
        self.assertTrue(s.remove(2))
        self.assertFalse(s.contains(2))
        self.assertEqual(len(s), 4)
        self.assertFalse(s.remove(2))

    def test_remove_interval(self):
        s = IntervalSet()
        s.insert(0, 10)
        s.remove_interval(3, 6)  # remove [3,6)
        self.assertEqual(len(s), 7)
        for x in [0, 1, 2, 6, 7, 8, 9]:
            self.assertTrue(s.contains(x))
        for x in [3, 4, 5]:
            self.assertFalse(s.contains(x))

    def test_mex(self):
        s = IntervalSet()
        s.insert(0, 3)  # {0,1,2}
        self.assertEqual(s.mex(0), 3)
        s.add(4)
        self.assertEqual(s.mex(4), 5)
        self.assertEqual(s.mex(3), 3)

    def test_expand(self):
        s = IntervalSet()
        s.insert(2, 5)  # [2,5)
        self.assertEqual(s.expand(3), (2, 5))
        self.assertEqual(s.expand(10), (10, 10))

    def test_matches_boolean_array_randomized(self):
        """add/remove/insert/remove_interval/mex/expand/lenが
        真偽値配列の参照実装と一致することをランダムに確認する"""
        random.seed(3)
        n = 40
        ref = [False] * n
        s = IntervalSet()

        for _ in range(500):
            op = random.randint(0, 3)
            if op == 0:
                x = random.randint(0, n - 1)
                self.assertEqual(s.add(x), not ref[x])
                ref[x] = True
            elif op == 1:
                x = random.randint(0, n - 1)
                self.assertEqual(s.remove(x), ref[x])
                ref[x] = False
            elif op == 2:
                l = random.randint(0, n - 1)
                r = random.randint(l, n - 1) + 1
                s.insert(l, r)
                for i in range(l, r):
                    ref[i] = True
            else:
                l = random.randint(0, n - 1)
                r = random.randint(l, n - 1) + 1
                s.remove_interval(l, r)
                for i in range(l, r):
                    ref[i] = False

            self.assertEqual(len(s), sum(ref))
            for x in range(n):
                self.assertEqual(s.contains(x), ref[x])
            for x in range(n):
                m = x
                while m < n and ref[m]:
                    m += 1
                self.assertEqual(s.mex(x), m)


if __name__ == "__main__":
    unittest.main()
