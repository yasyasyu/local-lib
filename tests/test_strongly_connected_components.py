"""strongly_connected_components.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from strongly_connected_components import StronglyConnectedComponents


class TestStronglyConnectedComponents(unittest.TestCase):
    def _to_sets(self, groups):
        return sorted((tuple(sorted(g)) for g in groups))

    def test_single_cycle_is_one_component(self):
        scc = StronglyConnectedComponents(3)
        scc.add_edge(0, 1)
        scc.add_edge(1, 2)
        scc.add_edge(2, 0)
        self.assertEqual(self._to_sets(scc.components()), [(0, 1, 2)])

    def test_dag_each_node_is_own_component(self):
        scc = StronglyConnectedComponents(3)
        scc.add_edge(0, 1)
        scc.add_edge(1, 2)
        result = self._to_sets(scc.components())
        self.assertEqual(result, [(0,), (1,), (2,)])

    def test_two_components(self):
        scc = StronglyConnectedComponents(4)
        scc.add_edge(0, 1)
        scc.add_edge(1, 0)
        scc.add_edge(2, 3)
        scc.add_edge(3, 2)
        result = self._to_sets(scc.components())
        self.assertEqual(result, [(0, 1), (2, 3)])

    def test_components_are_in_topological_order(self):
        """成分間の辺は、リストの前の成分から後ろの成分へ向かうこと"""
        scc = StronglyConnectedComponents(5)
        scc.add_edge(3, 4)
        scc.add_edge(4, 3)
        scc.add_edge(4, 0)
        scc.add_edge(0, 1)
        scc.add_edge(1, 0)
        scc.add_edge(1, 2)
        groups = scc.components()
        index = {v: i for i, group in enumerate(groups) for v in group}
        for u in range(5):
            for v in scc.edge[u]:
                self.assertLessEqual(index[u], index[v])
        self.assertEqual(len(groups), 3)

    def test_isolated_vertex(self):
        scc = StronglyConnectedComponents(1)
        self.assertEqual(scc.components(), [[0]])

    def test_components_does_not_lower_recursion_limit(self):
        """components()呼び出しがグローバルな再帰上限を不用意に下げないこと"""
        before = sys.getrecursionlimit()
        scc = StronglyConnectedComponents(3)
        scc.add_edge(0, 1)
        scc.components()
        self.assertGreaterEqual(sys.getrecursionlimit(), before)


if __name__ == "__main__":
    unittest.main()
