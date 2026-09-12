"""euler_tour.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from euler_tour import euler_tour


class TestEulerTour(unittest.TestCase):
    def test_single_node(self):
        left_id, right_id, depth = euler_tour([[]], 0)
        self.assertEqual(depth, [0])

    def test_simple_tree_depths(self):
        # 0 -> 1, 2 ; 1 -> 3
        G = [[1, 2], [0, 3], [0], [1]]
        left_id, right_id, depth = euler_tour(G, 0)
        self.assertEqual(depth, [0, 1, 1, 2])

    def test_left_right_id_ranges_cover_subtree_size(self):
        """left_id/right_idの差が、その部分木に含まれる頂点数と一致すること"""
        G = [[1, 2], [0, 3, 4], [0], [1], [1]]
        left_id, right_id, depth = euler_tour(G, 0)
        subtree_size = {
            0: 5,  # 0,1,2,3,4
            1: 3,  # 1,3,4
            2: 1,
            3: 1,
            4: 1,
        }
        for v, size in subtree_size.items():
            self.assertEqual(right_id[v] - left_id[v], size, v)

    def test_chain(self):
        # 0 -> 1 -> 2 -> 3
        G = [[1], [0, 2], [1, 3], [2]]
        left_id, right_id, depth = euler_tour(G, 0)
        self.assertEqual(depth, [0, 1, 2, 3])


if __name__ == "__main__":
    unittest.main()
