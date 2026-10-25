"""hld.pyのテストコード

hld.pyは `from .tree_order import tree_order` という相対インポートを
使っているため、パッケージとしてインポートする必要がある。
親ディレクトリをsys.pathに追加し、フォルダ名前空間パッケージ経由で読み込む。
"""

import importlib
import random
import sys
import unittest
from pathlib import Path

_LIB_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_LIB_DIR.parent))

HLD = importlib.import_module(f"{_LIB_DIR.name}.hld").HLD


def random_tree(n, rng):
    G = [[] for _ in range(n)]
    for v in range(1, n):
        p = rng.randrange(v)
        G[p].append(v)
        G[v].append(p)
    return G


def rooted(G, root):
    n = len(G)
    parent = [-1] * n
    depth = [0] * n
    order = [root]
    for v in order:
        for u in G[v]:
            if u != parent[v]:
                parent[u] = v
                depth[u] = depth[v] + 1
                order.append(u)
    return parent, depth


def path_vertices(parent, depth, u, v):
    left, right = [], []
    while depth[u] > depth[v]:
        left.append(u)
        u = parent[u]
    while depth[v] > depth[u]:
        right.append(v)
        v = parent[v]
    while u != v:
        left.append(u)
        right.append(v)
        u, v = parent[u], parent[v]
    return left + [u] + right[::-1], u


def subtree_vertices(G, parent, v):
    res = [v]
    for x in res:
        for u in G[x]:
            if u != parent[x]:
                res.append(u)
    return res


class TestHLD(unittest.TestCase):
    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(100):
            n = rng.randint(1, 30)
            G = random_tree(n, rng)
            root = rng.randrange(n)
            hld = HLD(G, root)
            parent, depth = rooted(G, root)
            self.assertEqual(hld.parent, parent)
            self.assertEqual(hld.depth, depth)
            self.assertEqual(sorted(hld.index(v) for v in range(n)), list(range(n)))
            self.assertEqual([hld.order[hld.index(v)] for v in range(n)], list(range(n)))
            A = [rng.randint(1, 100) for _ in range(n)]
            seq = [A[hld.order[i]] for i in range(n)]
            for _ in range(30):
                u, v = rng.randrange(n), rng.randrange(n)
                verts, lca = path_vertices(parent, depth, u, v)
                self.assertEqual(hld.lca(u, v), lca)
                self.assertEqual(hld.dist(u, v), len(verts) - 1)
                # パスの区間は重ならず、ちょうどパス上の頂点を覆う
                covered = [i for l, r in hld.path(u, v) for i in range(l, r)]
                self.assertEqual(sorted(covered), sorted(hld.index(x) for x in verts))
                self.assertEqual(sum(seq[i] for i in covered), sum(A[x] for x in verts))
                covered_e = [i for l, r in hld.path(u, v, edge=True) for i in range(l, r)]
                self.assertEqual(sorted(covered_e), sorted(hld.index(x) for x in verts if x != lca))
                k = rng.randint(0, depth[u] + 2)
                want = u
                for _ in range(k):
                    want = parent[want] if want != -1 else -1
                self.assertEqual(hld.ancestor(u, k), want if k <= depth[u] else -1)
            for v in range(n):
                l, r = hld.subtree(v)
                self.assertEqual(sorted(hld.order[l:r]), sorted(subtree_vertices(G, parent, v)))
                le, re_ = hld.subtree(v, edge=True)
                self.assertEqual((le, re_), (l + 1, r))

    def test_path_has_log_segments(self):
        n = 1 << 12
        G = [[] for _ in range(n)]
        for v in range(1, n):
            p = (v - 1) // 2  # 完全二分木
            G[p].append(v)
            G[v].append(p)
        hld = HLD(G, 0)
        rng = random.Random(1)
        for _ in range(200):
            u, v = rng.randrange(n), rng.randrange(n)
            self.assertLessEqual(len(hld.path(u, v)), 2 * 12 + 2)

    def test_deep_path_without_recursion(self):
        n = 200000
        G = [[] for _ in range(n)]
        for v in range(1, n):
            G[v - 1].append(v)
            G[v].append(v - 1)
        hld = HLD(G, 0)
        self.assertEqual(hld.lca(n - 1, n // 2), n // 2)
        self.assertEqual(hld.path(0, n - 1), [(0, n)])
        self.assertEqual(hld.ancestor(n - 1, n - 1), 0)


if __name__ == "__main__":
    unittest.main()
