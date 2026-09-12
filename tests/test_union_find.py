"""union_find.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from union_find import UnionFind


class TestUnionFind(unittest.TestCase):
    def test_initial_state_all_singletons(self):
        uf = UnionFind(5)
        self.assertEqual(uf.groups(), [[0], [1], [2], [3], [4]])

    def test_merge_and_same(self):
        uf = UnionFind(5)
        uf.merge(0, 1)
        self.assertTrue(uf.same(0, 1))
        self.assertFalse(uf.same(0, 2))

    def test_merge_same_group_is_noop(self):
        uf = UnionFind(3)
        uf.merge(0, 1)
        uf.merge(1, 0)
        self.assertEqual(len(uf.groups()), 2)

    def test_groups_partitions_all_elements(self):
        """groups()が全要素を過不足なく分割すること（境界演算子の優先順位バグの回帰テスト）"""
        uf = UnionFind(6)
        uf.merge(0, 1)
        uf.merge(2, 3)
        uf.merge(1, 2)
        groups = uf.groups()
        flattened = sorted(x for g in groups for x in g)
        self.assertEqual(flattened, list(range(6)))
        self.assertTrue(uf.same(0, 3))
        self.assertFalse(uf.same(0, 4))

    def test_groups_matches_same_relation(self):
        uf = UnionFind(8)
        for a, b in [(0, 1), (1, 2), (3, 4), (5, 6), (6, 7)]:
            uf.merge(a, b)
        for group in uf.groups():
            for x in group:
                for y in group:
                    self.assertTrue(uf.same(x, y))
        roots = {uf.find(x) for x in range(8)}
        self.assertEqual(len(roots), len(uf.groups()))


if __name__ == "__main__":
    unittest.main()
