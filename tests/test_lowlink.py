"""lowlink.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lowlink import LowLink


def count_components(n, edges, removed_vertex=-1, removed_edge=-1):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, (u, v) in enumerate(edges):
        if i == removed_edge or u == removed_vertex or v == removed_vertex:
            continue
        parent[find(u)] = find(v)
    return len({find(v) for v in range(n) if v != removed_vertex})


def brute(n, edges):
    base = count_components(n, edges)
    bridges = [i for i in range(len(edges)) if count_components(n, edges, removed_edge=i) > base]
    # 頂点 v を除いたとき、v 自身の分の成分（孤立点なら1つ減る）を考えて比べる
    arts = []
    for v in range(n):
        isolated = all(v not in e for e in edges if e[0] != e[1])
        if count_components(n, edges, removed_vertex=v) > base - (1 if isolated else 0):
            arts.append(v)
    return bridges, arts


class TestLowLink(unittest.TestCase):
    def test_docstring_example(self):
        ll = LowLink(4, [(0, 1), (1, 2), (2, 0), (2, 3)])
        self.assertEqual(ll.bridges, [3])
        self.assertEqual(ll.articulation_points, [2])

    def test_path(self):
        ll = LowLink(4, [(0, 1), (1, 2), (2, 3)])
        self.assertEqual(ll.bridges, [0, 1, 2])
        self.assertEqual(ll.articulation_points, [1, 2])

    def test_multi_edge_is_not_bridge(self):
        ll = LowLink(3, [(0, 1), (0, 1), (1, 2)])
        self.assertEqual(ll.bridges, [2])
        self.assertEqual(ll.articulation_points, [1])

    def test_self_loop_and_isolated(self):
        ll = LowLink(3, [(0, 0), (1, 2)])
        self.assertEqual(ll.bridges, [1])
        self.assertEqual(ll.articulation_points, [])

    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(300):
            n = rng.randint(1, 9)
            m = rng.randint(0, 12)
            edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
            ll = LowLink(n, edges)
            bridges, arts = brute(n, edges)
            self.assertEqual(ll.bridges, bridges, edges)
            self.assertEqual(ll.articulation_points, arts, edges)

    def test_deep_path_without_recursion(self):
        n = 200000
        ll = LowLink(n, [(i, i + 1) for i in range(n - 1)])
        self.assertEqual(len(ll.bridges), n - 1)
        self.assertEqual(len(ll.articulation_points), n - 2)


if __name__ == "__main__":
    unittest.main()
