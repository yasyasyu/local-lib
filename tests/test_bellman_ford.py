"""bellman_ford.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bellman_ford import bellman_ford

INF = float("inf")
NEG_INF = float("-inf")


class TestBellmanFord(unittest.TestCase):
    def test_simple_path(self):
        edges = [(0, 1, 1), (1, 2, 1)]
        dist = bellman_ford(edges, 3, 0)
        self.assertEqual(dist, [0, 1, 2])

    def test_unreachable_vertex_is_inf(self):
        edges = [(0, 1, 1)]
        dist = bellman_ford(edges, 3, 0)
        self.assertEqual(dist, [0, 1, INF])

    def test_negative_edge_without_cycle(self):
        edges = [(0, 1, 3), (1, 2, -2)]
        dist = bellman_ford(edges, 3, 0)
        self.assertEqual(dist, [0, 3, 1])

    def test_negative_cycle_reachable_from_start(self):
        edges = [(0, 1, 1), (1, 2, -3), (2, 1, 1)]  # 1<->2 が負閉路
        dist = bellman_ford(edges, 3, 0)
        self.assertEqual(dist[0], 0)
        self.assertEqual(dist[1], NEG_INF)
        self.assertEqual(dist[2], NEG_INF)

    def test_negative_cycle_not_reachable_from_start_is_unaffected(self):
        edges = [(1, 2, -1), (2, 1, -1)]  # 1<->2 が負閉路だが0からは行けない
        dist = bellman_ford(edges, 3, 0)
        self.assertEqual(dist, [0, INF, INF])

    def test_negative_cycle_effect_propagates_downstream(self):
        edges = [(0, 1, 1), (1, 1, -1), (1, 2, 1)]  # 1に自己負閉路、2はその先
        dist = bellman_ford(edges, 3, 0)
        self.assertEqual(dist[1], NEG_INF)
        self.assertEqual(dist[2], NEG_INF)


if __name__ == "__main__":
    unittest.main()
