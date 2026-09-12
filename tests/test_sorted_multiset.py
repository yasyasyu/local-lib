"""sorted_multi_set.pyのテストコード"""

import bisect
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sorted_multi_set import SortedMultiset


class TestSortedMultiset(unittest.TestCase):
    def test_construct_keeps_duplicates_sorted(self):
        sm = SortedMultiset([3, 1, 2, 1, 3])
        self.assertEqual(list(sm), [1, 1, 2, 3, 3])
        self.assertEqual(len(sm), 5)

    def test_add_keeps_duplicates(self):
        sm = SortedMultiset()
        sm.add(5)
        sm.add(5)
        self.assertEqual(len(sm), 2)
        self.assertEqual(sm.count(5), 2)

    def test_discard_removes_single_occurrence(self):
        sm = SortedMultiset([1, 1, 2])
        self.assertTrue(sm.discard(1))
        self.assertEqual(list(sm), [1, 2])
        self.assertFalse(sm.discard(3))

    def test_count(self):
        sm = SortedMultiset([1, 2, 2, 2, 3])
        self.assertEqual(sm.count(2), 3)
        self.assertEqual(sm.count(4), 0)

    def test_lt_le_gt_ge(self):
        sm = SortedMultiset([1, 3, 3, 5])
        self.assertEqual(sm.lt(3), 1)
        self.assertEqual(sm.le(3), 3)
        self.assertEqual(sm.gt(3), 5)
        self.assertEqual(sm.ge(3), 3)

    def test_getitem_and_pop(self):
        sm = SortedMultiset([1, 2, 2, 3])
        self.assertEqual(sm[1], 2)
        self.assertEqual(sm.pop(0), 1)
        self.assertEqual(list(sm), [2, 2, 3])

    def test_index_and_index_right(self):
        sm = SortedMultiset([1, 2, 2, 4])
        self.assertEqual(sm.index(2), 1)
        self.assertEqual(sm.index_right(2), 3)

    def test_matches_bisect_insort_randomized(self):
        random.seed(2)
        ref = []
        sm = SortedMultiset()
        for _ in range(2000):
            op = random.randint(0, 2)
            x = random.randint(0, 200)
            if op == 0:
                sm.add(x)
                bisect.insort(ref, x)
            elif op == 1:
                was = x in ref
                self.assertEqual(sm.discard(x), was)
                if was:
                    ref.remove(x)
            else:
                self.assertEqual(sm.count(x), ref.count(x))
            self.assertEqual(len(sm), len(ref))
        self.assertEqual(list(sm), ref)


if __name__ == "__main__":
    unittest.main()
