"""topological_sort.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from topological_sort import topological_sort


def is_valid_topological_order(es, order):
    if sorted(order) != list(range(len(es))):
        return False
    position = {v: i for i, v in enumerate(order)}
    for u in range(len(es)):
        for v in es[u]:
            if position[u] >= position[v]:
                return False
    return True


class TestTopologicalSort(unittest.TestCase):
    def test_simple_chain(self):
        es = [[1], [2], []]
        self.assertEqual(topological_sort(es), [0, 1, 2])

    def test_diamond_shape(self):
        es = [[1, 2], [3], [3], []]
        order = topological_sort(es)
        self.assertTrue(is_valid_topological_order(es, order))

    def test_no_edges(self):
        es = [[], [], []]
        order = topological_sort(es)
        self.assertEqual(sorted(order), [0, 1, 2])

    def test_disconnected_components(self):
        es = [[1], [], [3], []]
        order = topological_sort(es)
        self.assertTrue(is_valid_topological_order(es, order))


if __name__ == "__main__":
    unittest.main()
