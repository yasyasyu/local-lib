"""zero_one_bfs.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dijkstra import dijkstra
from zero_one_bfs import zero_one_bfs

INF = float("inf")


class TestZeroOneBfs(unittest.TestCase):
    def test_simple(self):
        G = [[(1, 1), (2, 0)], [], [(1, 0)]]
        self.assertEqual(zero_one_bfs(G, 0), [0, 0, 0])

    def test_unreachable_is_inf(self):
        G = [[(1, 1)], [], []]
        self.assertEqual(zero_one_bfs(G, 0), [0, 1, INF])

    def test_random_matches_dijkstra(self):
        rng = random.Random(0)
        for _ in range(300):
            n = rng.randint(1, 15)
            G = [[] for _ in range(n)]
            for _ in range(rng.randint(0, 40)):
                G[rng.randrange(n)].append((rng.randrange(n), rng.randint(0, 1)))
            s = rng.randrange(n)
            self.assertEqual(zero_one_bfs(G, s), dijkstra(G, s))


if __name__ == "__main__":
    unittest.main()
