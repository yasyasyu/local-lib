"""lca.pyのテストコード

lca.pyは `from .doubling import Doubling` という相対インポートを
使っているため、パッケージとしてインポートする必要がある。
親ディレクトリをsys.pathに追加し、フォルダ名前空間パッケージ経由で読み込む。
"""

import importlib
import sys
import unittest
from pathlib import Path

_LIB_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_LIB_DIR.parent))

LCA = importlib.import_module(f"{_LIB_DIR.name}.lca").LCA


def _tree_graph():
    #        0
    #      /   \
    #     1     2
    #    / \
    #   3   4
    return [[1, 2], [0, 3, 4], [0], [1], [1]]


class TestLCA(unittest.TestCase):
    def test_siblings(self):
        lca = LCA(_tree_graph(), root=0)
        self.assertEqual(lca.query(3, 4), 1)

    def test_cousins(self):
        lca = LCA(_tree_graph(), root=0)
        self.assertEqual(lca.query(3, 2), 0)

    def test_ancestor_and_descendant(self):
        lca = LCA(_tree_graph(), root=0)
        self.assertEqual(lca.query(0, 4), 0)
        self.assertEqual(lca.query(4, 1), 1)

    def test_same_node(self):
        lca = LCA(_tree_graph(), root=0)
        self.assertEqual(lca.query(3, 3), 3)

    def test_depth(self):
        lca = LCA(_tree_graph(), root=0)
        self.assertEqual(lca.depth, [0, 1, 1, 2, 2])

    def test_distance(self):
        lca = LCA(_tree_graph(), root=0)
        self.assertEqual(lca.distance(3, 4), 2)
        self.assertEqual(lca.distance(3, 2), 3)
        self.assertEqual(lca.distance(0, 4), 2)

    def test_single_node(self):
        lca = LCA([[]], root=0)
        self.assertEqual(lca.query(0, 0), 0)

    def test_matches_brute_force_randomized(self):
        import random

        random.seed(0)
        for _ in range(20):
            n = random.randint(1, 30)
            G = [[] for _ in range(n)]
            parent = [-1] * n
            for v in range(1, n):
                p = random.randint(0, v - 1)
                parent[v] = p
                G[v].append(p)
                G[p].append(v)

            def brute_ancestors(v):
                anc = []
                while v != -1:
                    anc.append(v)
                    v = parent[v]
                return anc

            lca = LCA(G, root=0)
            for _ in range(20):
                u, v = random.randint(0, n - 1), random.randint(0, n - 1)
                anc_u = set(brute_ancestors(u))
                expected = next(a for a in brute_ancestors(v) if a in anc_u)
                self.assertEqual(lca.query(u, v), expected, (u, v))


if __name__ == "__main__":
    unittest.main()
