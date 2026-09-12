"""bucket_list.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bucket_list import BucketList


class TestBucketList(unittest.TestCase):
    def test_append_and_iteration(self):
        bl = BucketList()
        for x in [3, 1, 2]:
            bl.append(x)
        self.assertEqual(list(bl), [3, 1, 2])
        self.assertEqual(len(bl), 3)

    def test_insert_and_getitem(self):
        bl = BucketList([1, 2, 4])
        bl.insert(2, 3)
        self.assertEqual(list(bl), [1, 2, 3, 4])
        self.assertEqual(bl[2], 3)
        self.assertEqual(bl[-1], 4)

    def test_pop(self):
        bl = BucketList([1, 2, 3])
        self.assertEqual(bl.pop(), 3)
        self.assertEqual(bl.pop(0), 1)
        self.assertEqual(list(bl), [2])

    def test_contains_count_index(self):
        bl = BucketList([1, 2, 2, 3])
        self.assertIn(2, bl)
        self.assertNotIn(5, bl)
        self.assertEqual(bl.count(2), 2)
        self.assertEqual(bl.index(2), 1)
        with self.assertRaises(ValueError):
            bl.index(5)

    def test_remove(self):
        bl = BucketList([1, 2, 3])
        bl.remove(2)
        self.assertEqual(list(bl), [1, 3])

    def test_reverse_and_copy(self):
        bl = BucketList([1, 2, 3])
        bl.reverse()
        self.assertEqual(list(bl), [3, 2, 1])
        copied = bl.copy()
        copied.append(0)
        self.assertEqual(list(bl), [3, 2, 1])
        self.assertEqual(list(copied), [3, 2, 1, 0])

    def test_matches_python_list_randomized(self):
        """挿入/削除/参照をランダム実行し、Pythonのlistと結果が一致することを確認"""
        random.seed(0)
        ref = []
        bl = BucketList()
        for _ in range(1000):
            op = random.randint(0, 3)
            if op == 0:
                i = random.randint(0, len(ref))
                x = random.randint(0, 100)
                bl.insert(i, x)
                ref.insert(i, x)
            elif op == 1:
                x = random.randint(0, 100)
                bl.append(x)
                ref.append(x)
            elif op == 2 and ref:
                i = random.randint(-len(ref), len(ref) - 1)
                self.assertEqual(bl.pop(i), ref.pop(i))
            elif op == 3 and ref:
                i = random.randint(-len(ref), len(ref) - 1)
                self.assertEqual(bl[i], ref[i])
            self.assertEqual(len(bl), len(ref))
        self.assertEqual(list(bl), ref)


if __name__ == "__main__":
    unittest.main()
