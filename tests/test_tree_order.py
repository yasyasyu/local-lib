"""tree_order.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tree_order import tree_order


def random_tree(n, rng):
    G = [[] for _ in range(n)]
    for v in range(1, n):
        p = rng.randrange(v)
        G[p].append(v)
        G[v].append(p)
    return G


class TestTreeOrder(unittest.TestCase):
    def test_single_vertex(self):
        self.assertEqual(tree_order([[]], 0), ([0], [-1]))

    def test_small(self):
        # 0 - 1 - 3, 0 - 2
        G = [[1, 2], [0, 3], [0], [1]]
        order, parent = tree_order(G, 0)
        self.assertEqual(order, [0, 1, 2, 3])
        self.assertEqual(parent, [-1, 0, 0, 1])

    def test_other_root(self):
        G = [[1, 2], [0, 3], [0], [1]]
        order, parent = tree_order(G, 3)
        self.assertEqual(order[0], 3)
        self.assertEqual(parent, [1, 3, 0, -1])

    def test_random_parent_before_child_and_bfs(self):
        rng = random.Random(0)
        for _ in range(100):
            n = rng.randint(1, 30)
            G = random_tree(n, rng)
            root = rng.randrange(n)
            order, parent = tree_order(G, root)
            self.assertEqual(sorted(order), list(range(n)))
            pos = {v: i for i, v in enumerate(order)}
            depth = [0] * n
            for v in order[1:]:
                self.assertLess(pos[parent[v]], pos[v])
                self.assertIn(parent[v], G[v])
                depth[v] = depth[parent[v]] + 1
            # BFS 順なので、深さが単調非減少
            self.assertEqual([depth[v] for v in order], sorted(depth[v] for v in order))

    def test_deep_path_without_recursion(self):
        n = 200000
        G = [[] for _ in range(n)]
        for v in range(1, n):
            G[v - 1].append(v)
            G[v].append(v - 1)
        order, parent = tree_order(G, 0)
        self.assertEqual(order, list(range(n)))
        self.assertEqual(parent[-1], n - 2)


if __name__ == "__main__":
    unittest.main()
