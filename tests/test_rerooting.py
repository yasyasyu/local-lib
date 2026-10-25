"""rerooting.pyのテストコード

rerooting.pyは `from .tree_order import tree_order` という相対インポートを
使っているため、パッケージとしてインポートする必要がある。
親ディレクトリをsys.pathに追加し、フォルダ名前空間パッケージ経由で読み込む。
"""

import importlib
import random
import sys
import unittest
from collections import deque
from pathlib import Path

_LIB_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_LIB_DIR.parent))

rerooting = importlib.import_module(f"{_LIB_DIR.name}.rerooting").rerooting


def random_tree(n, rng):
    G = [[] for _ in range(n)]
    edges = []
    for v in range(1, n):
        p = rng.randrange(v)
        G[p].append(v)
        G[v].append(p)
        edges.append((p, v))
    return G, edges


def bfs_dist(G, s, W=None):
    dist = [-1] * len(G)
    dist[s] = 0
    q = deque([s])
    while q:
        v = q.popleft()
        for u in G[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + (W[(v, u)] if W else 1)
                q.append(u)
    return dist


def dist_sum_rerooting(G):
    ans = rerooting(
        G,
        op=lambda a, b: (a[0] + b[0], a[1] + b[1]),
        e=(0, 0),
        add_vertex=lambda x, v: (x[0] + 1, x[1]),
        add_edge=lambda x, frm, to: (x[0], x[1] + x[0]),
    )
    return [s for _, s in ans]


class TestRerooting(unittest.TestCase):
    def test_single_vertex(self):
        self.assertEqual(dist_sum_rerooting([[]]), [0])

    def test_abc220f_sample(self):
        # 1-2, 2-3 の木（0-indexed で 0-1, 1-2）
        G = [[1], [0, 2], [1]]
        self.assertEqual(dist_sum_rerooting(G), [3, 2, 3])

    def test_dist_sum_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(100):
            n = rng.randint(1, 25)
            G, _ = random_tree(n, rng)
            want = [sum(bfs_dist(G, s)) for s in range(n)]
            self.assertEqual(dist_sum_rerooting(G), want)

    def test_eccentricity_without_add_edge(self):
        # 高さ: 葉は0。add_edge を省略し、add_vertex で +1 する（e = -1 で葉が 0 になる）
        rng = random.Random(1)
        for _ in range(100):
            n = rng.randint(1, 25)
            G, _ = random_tree(n, rng)
            got = rerooting(G, max, -1, lambda x, v: x + 1)
            want = [max(bfs_dist(G, s)) for s in range(n)]
            self.assertEqual(got, want)

    def test_weighted_eccentricity(self):
        rng = random.Random(2)
        for _ in range(100):
            n = rng.randint(1, 25)
            G, edges = random_tree(n, rng)
            W = {}
            for u, v in edges:
                W[(u, v)] = W[(v, u)] = rng.randint(1, 9)
            got = rerooting(G, max, 0, lambda x, v: x, lambda x, frm, to: x + W[(frm, to)])
            want = [max(bfs_dist(G, s, W)) for s in range(n)]
            self.assertEqual(got, want)

    def test_deep_path_without_recursion(self):
        n = 100000
        G = [[] for _ in range(n)]
        for v in range(1, n):
            G[v - 1].append(v)
            G[v].append(v - 1)
        got = dist_sum_rerooting(G)
        self.assertEqual(got[0], n * (n - 1) // 2)
        self.assertEqual(got[n // 2], (n // 2) * (n // 2 + 1) // 2 + (n - 1 - n // 2) * (n - n // 2) // 2)


if __name__ == "__main__":
    unittest.main()
