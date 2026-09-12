"""kruskal.pyのテストコード

kruskal.pyは `from .union_find import UnionFind` という相対インポートを
使っているため、パッケージとしてインポートする必要がある。
親ディレクトリをsys.pathに追加し、フォルダ名前空間パッケージ経由で読み込む。
"""

import importlib
import sys
import unittest
from pathlib import Path

_LIB_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_LIB_DIR.parent))

kruskal = importlib.import_module(f"{_LIB_DIR.name}.kruskal").kruskal


class TestKruskal(unittest.TestCase):
    def test_simple_triangle_picks_two_cheapest_edges(self):
        edges = [(3, 0, 1), (1, 1, 2), (2, 0, 2)]
        total_cost, used_edges = kruskal(edges, 3)
        self.assertEqual(total_cost, 3)
        self.assertEqual(sorted(used_edges), [(1, 1, 2), (2, 0, 2)])

    def test_disconnected_graph_forms_minimum_spanning_forest(self):
        edges = [(1, 0, 1), (1, 2, 3)]
        total_cost, used_edges = kruskal(edges, 4)
        self.assertEqual(total_cost, 2)
        self.assertEqual(len(used_edges), 2)

    def test_no_edges(self):
        total_cost, used_edges = kruskal([], 3)
        self.assertEqual(total_cost, 0)
        self.assertEqual(used_edges, [])

    def test_duplicate_edge_is_skipped_if_cycle(self):
        edges = [(1, 0, 1), (1, 0, 1), (5, 1, 2)]
        total_cost, used_edges = kruskal(edges, 3)
        self.assertEqual(total_cost, 6)
        self.assertEqual(len(used_edges), 2)


if __name__ == "__main__":
    unittest.main()
