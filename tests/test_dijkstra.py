"""dijkstra.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dijkstra import dijkstra

INF = float("inf")


class TestDijkstra(unittest.TestCase):
    def test_simple_path(self):
        G = [[(1, 1)], [(2, 1)], []]
        dist = dijkstra(G, 0)
        self.assertEqual(dist, [0, 1, 2])

    def test_unreachable_vertex_is_inf(self):
        G = [[(1, 1)], [], [(1, 1)]]
        dist = dijkstra(G, 0)
        self.assertEqual(dist, [0, 1, INF])

    def test_picks_shorter_path(self):
        # 0 -> 1 -> 2 (cost 2) vs 0 -> 2 (cost 10)
        G = [[(1, 1), (2, 10)], [(2, 1)], []]
        dist = dijkstra(G, 0)
        self.assertEqual(dist, [0, 1, 2])

    def test_undirected_graph(self):
        G = [[(1, 5)], [(0, 5), (2, 3)], [(1, 3)]]
        dist = dijkstra(G, 2)
        self.assertEqual(dist, [8, 3, 0])

    def test_single_vertex(self):
        self.assertEqual(dijkstra([[]], 0), [0])


if __name__ == "__main__":
    unittest.main()
