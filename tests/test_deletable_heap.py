"""deletable_heap.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from deletable_heap import DeletableHeap


class TestDeletableHeap(unittest.TestCase):
    def test_push_and_get_min(self):
        h = DeletableHeap()
        h.push(3)
        h.push(1)
        h.push(2)
        self.assertEqual(h.get(), 1)
        self.assertEqual(len(h), 3)

    def test_pop_removes_min(self):
        h = DeletableHeap()
        for x in [3, 1, 2]:
            h.push(x)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(h.pop(), 3)
        self.assertEqual(len(h), 0)

    def test_discard(self):
        h = DeletableHeap()
        h.push(1)
        h.push(1)
        h.push(2)
        self.assertTrue(h.discard(1))
        self.assertEqual(h.count(1), 1)
        self.assertFalse(h.discard(5))

    def test_erase_multiple(self):
        h = DeletableHeap()
        for _ in range(3):
            h.push(4)
        removed = h.erase(4, 2)
        self.assertEqual(removed, 2)
        self.assertEqual(h.count(4), 1)

    def test_is_unique(self):
        h = DeletableHeap(is_unique=True)
        h.push(1)
        h.push(1)
        self.assertEqual(len(h), 1)
        self.assertEqual(h.count(1), 1)

    def test_sum_and_types(self):
        h = DeletableHeap()
        h.push(1)
        h.push(2)
        h.push(2)
        self.assertEqual(h.sum(), 5)
        self.assertEqual(h.types(), 2)

    def test_matches_reference_list_randomized(self):
        random.seed(4)
        h = DeletableHeap()
        ref = []
        for _ in range(1000):
            op = random.randint(0, 3)
            if op == 0:
                x = random.randint(0, 20)
                h.push(x)
                ref.append(x)
            elif op == 1 and ref:
                self.assertEqual(h.get(), min(ref))
            elif op == 2 and ref:
                m = min(ref)
                self.assertEqual(h.pop(), m)
                ref.remove(m)
            elif op == 3 and ref:
                x = random.choice(ref)
                n = random.randint(1, 3)
                expected = min(n, ref.count(x))
                self.assertEqual(h.erase(x, n), expected)
                for _ in range(expected):
                    ref.remove(x)
            self.assertEqual(len(h), len(ref))
            self.assertEqual(h.sum(), sum(ref))


if __name__ == "__main__":
    unittest.main()
