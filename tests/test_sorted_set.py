"""sorted_set.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sorted_set import SortedSet


class TestSortedSet(unittest.TestCase):
    def test_construct_deduplicates_and_sorts(self):
        ss = SortedSet([3, 1, 2, 1, 3])
        self.assertEqual(list(ss), [1, 2, 3])
        self.assertEqual(len(ss), 3)

    def test_add_returns_false_for_duplicate(self):
        ss = SortedSet()
        self.assertTrue(ss.add(5))
        self.assertFalse(ss.add(5))
        self.assertEqual(len(ss), 1)

    def test_discard(self):
        ss = SortedSet([1, 2, 3])
        self.assertTrue(ss.discard(2))
        self.assertFalse(ss.discard(2))
        self.assertEqual(list(ss), [1, 3])

    def test_contains(self):
        ss = SortedSet([1, 2, 3])
        self.assertIn(2, ss)
        self.assertNotIn(4, ss)

    def test_lt_le_gt_ge(self):
        ss = SortedSet([1, 3, 5, 7])
        self.assertEqual(ss.lt(5), 3)
        self.assertEqual(ss.le(5), 5)
        self.assertEqual(ss.gt(5), 7)
        self.assertEqual(ss.ge(5), 5)
        self.assertIsNone(ss.lt(1))
        self.assertIsNone(ss.gt(7))

    def test_getitem_and_pop(self):
        ss = SortedSet([1, 2, 3, 4])
        self.assertEqual(ss[0], 1)
        self.assertEqual(ss[-1], 4)
        self.assertEqual(ss.pop(), 4)
        self.assertEqual(list(ss), [1, 2, 3])

    def test_index_and_index_right(self):
        ss = SortedSet([1, 2, 4, 5])
        self.assertEqual(ss.index(4), 2)  # 4未満の要素数
        self.assertEqual(ss.index_right(4), 3)  # 4以下の要素数

    def test_matches_python_set_randomized(self):
        random.seed(1)
        ref = set()
        ss = SortedSet()
        for _ in range(2000):
            op = random.randint(0, 2)
            x = random.randint(0, 200)
            if op == 0:
                self.assertEqual(ss.add(x), x not in ref)
                ref.add(x)
            elif op == 1:
                self.assertEqual(ss.discard(x), x in ref)
                ref.discard(x)
            else:
                self.assertEqual(x in ss, x in ref)
            self.assertEqual(len(ss), len(ref))
        self.assertEqual(list(ss), sorted(ref))


if __name__ == "__main__":
    unittest.main()
