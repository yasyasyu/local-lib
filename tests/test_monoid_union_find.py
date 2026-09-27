"""monoid_union_find.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from monoid_union_find import MonoidUnionFind


class TestMonoidUnionFind(unittest.TestCase):
    def test_docstring_example_sum(self):
        uf = MonoidUnionFind(lambda a, b: a + b, [3, 1, 4, 1, 5])
        self.assertTrue(uf.merge(0, 1))
        self.assertEqual(uf.get(1), 4)
        self.assertEqual(uf.size(0), 2)
        self.assertEqual(uf.get(2), 4)

    def test_docstring_example_edge_count(self):
        uf = MonoidUnionFind(lambda a, b: (a[0] + b[0], a[1] + b[1]), [(1, 0)] * 4)
        results = []
        for u, v in [(0, 1), (1, 2), (2, 0)]:
            results.append(uf.merge(u, v))
            uf.apply(u, lambda d: (d[0], d[1] + 1))
        self.assertEqual(results, [True, True, False])
        self.assertEqual(uf.get(0), (3, 3))
        self.assertEqual(uf.get(3), (1, 0))

    def test_merge_same_set_returns_false_and_keeps_value(self):
        uf = MonoidUnionFind(min, [5, 2, 7])
        uf.merge(0, 1)
        self.assertFalse(uf.merge(1, 0))
        self.assertEqual(uf.get(0), 2)

    def test_matches_brute_force_randomized(self):
        random.seed(0)
        for op, gen in [
            (lambda a, b: a + b, lambda: random.randint(-10, 10)),
            (min, lambda: random.randint(-10, 10)),
            (max, lambda: random.randint(-10, 10)),
        ]:
            for n in [1, 2, 5, 30]:
                v = [gen() for _ in range(n)]
                uf = MonoidUnionFind(op, v)
                label = list(range(n))
                for _ in range(100):
                    x, y = random.randrange(n), random.randrange(n)
                    merged = uf.merge(x, y)
                    self.assertEqual(merged, label[x] != label[y])
                    old = label[y]
                    label = [label[x] if l == old else l for l in label]
                    for i in range(n):
                        members = [j for j in range(n) if label[j] == label[i]]
                        expected = v[members[0]]
                        for j in members[1:]:
                            expected = op(expected, v[j])
                        self.assertEqual(uf.get(i), expected)
                        self.assertEqual(uf.size(i), len(members))
                self.assertEqual(
                    sorted(map(sorted, uf.groups())),
                    sorted(
                        sorted(j for j in range(n) if label[j] == l) for l in set(label)
                    ),
                )


if __name__ == "__main__":
    unittest.main()
