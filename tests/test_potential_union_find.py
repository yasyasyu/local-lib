"""potential_union_find.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from potential_union_find import PotentialUnionFind


class TestPotentialUnionFind(unittest.TestCase):
    def test_dist_between_unconnected_components_is_inf(self):
        uf = PotentialUnionFind(3)
        self.assertEqual(uf.dist(0, 1), uf.INF)

    def test_unite_and_dist(self):
        uf = PotentialUnionFind(3)
        uf.unite(0, 1, 5)  # potential[1] - potential[0] = 5
        uf.unite(1, 2, 3)  # potential[2] - potential[1] = 3
        self.assertEqual(uf.dist(0, 1), 5)
        self.assertEqual(uf.dist(1, 0), -5)
        self.assertEqual(uf.dist(0, 2), 8)
        self.assertEqual(uf.dist(2, 0), -8)

    def test_size_after_unite(self):
        uf = PotentialUnionFind(4)
        uf.unite(0, 1, 1)
        uf.unite(1, 2, 1)
        self.assertEqual(uf.size(0), 3)
        self.assertEqual(uf.size(3), 1)

    def test_groups_partition(self):
        uf = PotentialUnionFind(5)
        uf.unite(0, 1, 0)
        uf.unite(2, 3, 0)
        groups = uf.groups()
        flattened = sorted(x for g in groups for x in g)
        self.assertEqual(flattened, list(range(5)))
        self.assertEqual(len(groups), 3)

    def test_groups_index_consistency(self):
        uf = PotentialUnionFind(4)
        uf.unite(0, 1, 0)
        groups, index = uf.groups_index()
        for gi, group in enumerate(groups):
            for member in group:
                self.assertEqual(index[uf.root(member)], gi)

    def test_group_size_matches_groups(self):
        uf = PotentialUnionFind(5)
        uf.unite(0, 1, 0)
        uf.unite(2, 3, 0)
        self.assertEqual(
            sorted(uf.group_size()), sorted(len(g) for g in uf.groups())
        )


if __name__ == "__main__":
    unittest.main()
