"""potential_union_find.pyのテストコード"""

import random
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


    def test_unite_returns_whether_merged(self):
        uf = PotentialUnionFind(3)
        self.assertTrue(uf.unite(0, 1, 2))
        self.assertFalse(uf.unite(1, 0, -2))

    def test_xor_group(self):
        uf = PotentialUnionFind(4, op=lambda a, b: a ^ b, inv=lambda a: a, e=0)
        uf.unite(0, 1, 5)
        uf.unite(2, 1, 3)
        self.assertEqual(uf.dist(0, 2), 5 ^ 3)
        self.assertEqual(uf.dist(2, 0), 5 ^ 3)
        self.assertEqual(uf.dist(0, 3), uf.INF)

    def test_matches_hidden_values_randomized(self):
        """各要素に正解の値g[x]を隠し持たせ、それと矛盾しない関係だけをuniteしてdistを照合する"""
        MOD = 998244353
        groups = [
            ("add", lambda a, b: a + b, lambda a: -a, 0, lambda: random.randint(-100, 100)),
            ("xor", lambda a, b: a ^ b, lambda a: a, 0, lambda: random.randint(0, 255)),
            (
                "affine",  # 非可換: (a, b)はx -> a*x + b。op(f, g)はfの後にg
                lambda f, g: (f[0] * g[0] % MOD, (g[0] * f[1] + g[1]) % MOD),
                lambda f: (pow(f[0], -1, MOD), -pow(f[0], -1, MOD) * f[1] % MOD),
                (1, 0),
                lambda: (random.randint(1, MOD - 1), random.randint(0, MOD - 1)),
            ),
        ]
        random.seed(0)
        for name, op, inv, e, gen in groups:
            for n in [1, 2, 5, 40]:
                g = [gen() for _ in range(n)]
                uf = PotentialUnionFind(n, inf=None, op=op, inv=inv, e=e)
                label = list(range(n))
                for _ in range(150):
                    a, b = random.randrange(n), random.randrange(n)
                    if random.random() < 0.5:
                        uf.unite(a, b, op(inv(g[a]), g[b]))
                        old = label[b]
                        label = [label[a] if l == old else l for l in label]
                    else:
                        expected = op(inv(g[a]), g[b]) if label[a] == label[b] else None
                        self.assertEqual(uf.dist(a, b), expected, (name, n, a, b))


if __name__ == "__main__":
    unittest.main()
