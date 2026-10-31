"""tree_dp.pyのテストコード

tree_dp.pyは `from .tree_order import tree_order` という相対インポートを
使っているため、パッケージとしてインポートする必要がある。
親ディレクトリをsys.pathに追加し、フォルダ名前空間パッケージ経由で読み込む。
"""

import importlib
import random
import sys
import unittest
from collections import Counter, deque
from pathlib import Path

_LIB_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_LIB_DIR.parent))

tree_dp = importlib.import_module(f"{_LIB_DIR.name}.tree_dp").tree_dp
rerooting_tree_dp = importlib.import_module(f"{_LIB_DIR.name}.rerooting_tree_dp").rerooting_tree_dp


def random_tree(n, rng):
    G = [[] for _ in range(n)]
    edges = []
    for v in range(1, n):
        p = rng.randrange(v)
        G[p].append(v)
        G[v].append(p)
        edges.append((p, v))
    return G, edges


def bfs_parent(G, root):
    parent = [-1] * len(G)
    seen = [False] * len(G)
    seen[root] = True
    q = deque([root])
    while q:
        v = q.popleft()
        for u in G[v]:
            if not seen[u]:
                seen[u] = True
                parent[u] = v
                q.append(u)
    return parent


def ancestors(parent, v):
    """v 自身から根までの頂点を、近い順に返す"""
    path = [v]
    while parent[path[-1]] != -1:
        path.append(parent[path[-1]])
    return path


def all_dist(G):
    n = len(G)
    dist = []
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            for u in G[v]:
                if d[u] == -1:
                    d[u] = d[v] + 1
                    q.append(u)
        dist.append(d)
    return dist


def diameter_by_tree_dp(G):
    # docstring の使い方と同じ
    def merge_longest(a, b):
        if a is None:
            return b
        a_height, a_length = a
        b_height, b_length = b
        return max(a_height, b_height), max(a_length, b_length, a_height + b_height)

    _, D = tree_dp(
        G,
        op=merge_longest,
        e=None,
        add_vertex=lambda x, v: merge_longest(x, (0, 0)),
        add_edge=lambda x, frm, to: (x[0] + 1, x[1]),
    )[0]
    return D


def same_color_diameter_pairs_by_tree_dp(G, C):
    # docstring の使い方と同じ
    D = diameter_by_tree_dp(G)

    def merge_deepest(a, b):
        if a is None:
            return b
        a_height, a_colors, a_pairs = a
        b_height, b_colors, b_pairs = b
        pairs = a_pairs + b_pairs
        if len(a_colors) < len(b_colors):
            a_height, a_colors, b_height, b_colors = b_height, b_colors, a_height, a_colors
        if a_height + b_height == D:
            pairs += sum(m * a_colors[k] for k, m in b_colors.items())
        if a_height > b_height:
            return a_height, a_colors, pairs
        if a_height < b_height:
            return b_height, b_colors, pairs
        for k, m in b_colors.items():
            a_colors[k] += m
        return a_height, a_colors, pairs

    dp = tree_dp(
        G,
        op=merge_deepest,
        e=None,
        add_vertex=lambda x, v: merge_deepest(x, (0, Counter({C[v]: 1}), 0)),
        add_edge=lambda x, frm, to: (x[0] + 1, x[1], x[2]),
    )
    _, _, ans = dp[0]
    return ans


def max_independent_set_brute(G):
    n = len(G)
    best = 0
    for mask in range(1 << n):
        if all(not (mask >> v & 1 and mask >> u & 1) for v in range(n) for u in G[v]):
            best = max(best, bin(mask).count("1"))
    return best


class TestTreeDP(unittest.TestCase):
    def test_single_vertex(self):
        self.assertEqual(tree_dp([[]], lambda a, b: a + b, 0, lambda x, v: x + 1), [1])

    def test_subtree_size_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(100):
            n = rng.randint(1, 25)
            G, _ = random_tree(n, rng)
            root = rng.randrange(n)
            parent = bfs_parent(G, root)
            want = [0] * n
            for w in range(n):
                for a in ancestors(parent, w):
                    want[a] += 1
            got = tree_dp(G, lambda a, b: a + b, 0, lambda x, v: x + 1, root=root)
            self.assertEqual(got, want)

    def test_height_matches_brute_force(self):
        rng = random.Random(1)
        for _ in range(100):
            n = rng.randint(1, 25)
            G, _ = random_tree(n, rng)
            root = rng.randrange(n)
            parent = bfs_parent(G, root)
            want = [0] * n
            for w in range(n):
                for k, a in enumerate(ancestors(parent, w)):
                    want[a] = max(want[a], k)
            got = tree_dp(G, max, -1, lambda x, v: x + 1, root=root)
            self.assertEqual(got, want)

    def test_max_independent_set(self):
        rng = random.Random(2)
        for _ in range(100):
            n = rng.randint(1, 12)
            G, _ = random_tree(n, rng)
            dp = tree_dp(
                G,
                op=lambda a, b: (a[0] + b[0], a[1] + b[1]),
                e=(0, 0),
                add_vertex=lambda x, v: (x[0], x[1] + 1),
                add_edge=lambda x, frm, to: (max(x), x[0]),
            )
            self.assertEqual(max(dp[0]), max_independent_set_brute(G))

    def test_diameter(self):
        rng = random.Random(4)
        for _ in range(100):
            n = rng.randint(1, 25)
            G, _ = random_tree(n, rng)
            want = max(max(d) for d in all_dist(G))
            self.assertEqual(diameter_by_tree_dp(G), want)

    def test_same_color_diameter_pairs(self):
        rng = random.Random(5)
        for _ in range(300):
            n = rng.randint(1, 15)
            G, _ = random_tree(n, rng)
            C = [rng.randint(1, rng.randint(1, n)) for _ in range(n)]
            dist = all_dist(G)
            D = max(max(d) for d in dist)
            want = sum(
                1 for u in range(n) for v in range(u + 1, n) if C[u] == C[v] and dist[u][v] == D
            )
            self.assertEqual(same_color_diameter_pairs_by_tree_dp(G, C), want)

    def test_star_same_color_diameter_pairs(self):
        # 星: 葉どうしがすべて距離 2 の組になる。マージテクがないと O(N^2) になる形
        n = 100000
        G = [[] for _ in range(n)]
        for v in range(1, n):
            G[0].append(v)
            G[v].append(0)
        C = [v % 3 for v in range(n)]
        leaves = Counter(C[1:])
        want = sum(m * (m - 1) // 2 for m in leaves.values())
        self.assertEqual(same_color_diameter_pairs_by_tree_dp(G, C), want)

    def test_root_value_matches_rerooting_tree_dp(self):
        # 重み付きで、根から一番遠い頂点までの距離
        rng = random.Random(3)
        for _ in range(100):
            n = rng.randint(1, 25)
            G, edges = random_tree(n, rng)
            W = {}
            for u, v in edges:
                W[(u, v)] = W[(v, u)] = rng.randint(1, 9)
            args = (G, max, 0, lambda x, v: x, lambda x, frm, to: x + W[(frm, to)])
            all_roots = rerooting_tree_dp(*args)
            for root in range(n):
                self.assertEqual(tree_dp(*args, root=root)[root], all_roots[root])

    def test_deep_path_without_recursion(self):
        n = 100000
        G = [[] for _ in range(n)]
        for v in range(1, n):
            G[v - 1].append(v)
            G[v].append(v - 1)
        size = tree_dp(G, lambda a, b: a + b, 0, lambda x, v: x + 1)
        self.assertEqual(size, list(range(n, 0, -1)))


if __name__ == "__main__":
    unittest.main()
