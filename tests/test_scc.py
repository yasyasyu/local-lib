"""scc.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scc import SCC


class TestSCC(unittest.TestCase):
    def _to_sets(self, groups):
        return sorted((tuple(sorted(g)) for g in groups))

    def test_single_cycle_is_one_component(self):
        scc = SCC(3)
        scc.connect(0, 1)
        scc.connect(1, 2)
        scc.connect(2, 0)
        self.assertEqual(self._to_sets(scc.solve()), [(0, 1, 2)])

    def test_dag_each_node_is_own_component(self):
        scc = SCC(3)
        scc.connect(0, 1)
        scc.connect(1, 2)
        result = self._to_sets(scc.solve())
        self.assertEqual(result, [(0,), (1,), (2,)])

    def test_two_components(self):
        scc = SCC(4)
        scc.connect(0, 1)
        scc.connect(1, 0)
        scc.connect(2, 3)
        scc.connect(3, 2)
        result = self._to_sets(scc.solve())
        self.assertEqual(result, [(0, 1), (2, 3)])

    def test_isolated_vertex(self):
        scc = SCC(1)
        self.assertEqual(scc.solve(), [[0]])

    def test_solve_does_not_lower_recursion_limit(self):
        """solve()呼び出しがグローバルな再帰上限を不用意に下げないこと"""
        before = sys.getrecursionlimit()
        scc = SCC(3)
        scc.connect(0, 1)
        scc.solve()
        self.assertGreaterEqual(sys.getrecursionlimit(), before)


if __name__ == "__main__":
    unittest.main()
