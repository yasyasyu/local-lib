"""warshall_floyd.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from warshall_floyd import warshall_floyd

INF = float("inf")


class TestWarshallFloyd(unittest.TestCase):
    def test_simple_chain(self):
        G = [
            [0, 3, INF],
            [3, 0, 1],
            [INF, 1, 0],
        ]
        dist = warshall_floyd(G)
        self.assertEqual(dist[0][2], 4)
        self.assertEqual(dist[2][0], 4)

    def test_unreachable_pair_stays_inf(self):
        G = [
            [0, 1, INF],
            [1, 0, INF],
            [INF, INF, 0],
        ]
        dist = warshall_floyd(G)
        self.assertEqual(dist[0][2], INF)
        self.assertEqual(dist[2][0], INF)

    def test_direct_edge_replaced_by_shorter_indirect_path(self):
        G = [
            [0, 10, 1],
            [10, 0, 1],
            [1, 1, 0],
        ]
        dist = warshall_floyd(G)
        self.assertEqual(dist[0][1], 2)

    def test_does_not_mutate_input(self):
        G = [[0, 5], [5, 0]]
        original = [row[:] for row in G]
        warshall_floyd(G)
        self.assertEqual(G, original)


if __name__ == "__main__":
    unittest.main()
