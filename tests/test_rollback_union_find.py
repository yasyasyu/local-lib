"""rollback_union_find.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rollback_union_find import RollbackUnionFind


class TestRollbackUnionFind(unittest.TestCase):
    def test_initial_state_all_singletons(self):
        uf = RollbackUnionFind(5)
        for i in range(5):
            self.assertEqual(uf.size(i), 1)
        self.assertFalse(uf.same(0, 1))

    def test_merge_and_same(self):
        uf = RollbackUnionFind(5)
        uf.merge(0, 1)
        self.assertTrue(uf.same(0, 1))
        self.assertFalse(uf.same(0, 2))
        self.assertEqual(uf.size(0), 2)

    def test_merge_same_group_returns_false(self):
        uf = RollbackUnionFind(3)
        uf.merge(0, 1)
        self.assertFalse(uf.merge(1, 0))

    def test_undo_reverts_last_merge(self):
        uf = RollbackUnionFind(3)
        uf.merge(0, 1)
        uf.merge(1, 2)
        self.assertTrue(uf.same(0, 2))
        uf.undo()
        self.assertFalse(uf.same(0, 2))
        self.assertTrue(uf.same(0, 1))

    def test_undo_of_noop_merge_does_not_disturb_state(self):
        uf = RollbackUnionFind(3)
        uf.merge(0, 1)
        uf.merge(0, 1)  # no-op, since already same set
        uf.undo()
        self.assertTrue(uf.same(0, 1))
        self.assertEqual(uf.size(0), 2)

    def test_rollback_to_snapshot(self):
        uf = RollbackUnionFind(5)
        uf.merge(0, 1)
        state = uf.snapshot()
        uf.merge(1, 2)
        uf.merge(2, 3)
        self.assertTrue(uf.same(0, 3))
        uf.rollback(state)
        self.assertTrue(uf.same(0, 1))
        self.assertFalse(uf.same(0, 2))
        self.assertFalse(uf.same(0, 3))

    def test_rollback_to_initial_state(self):
        uf = RollbackUnionFind(4)
        uf.merge(0, 1)
        uf.merge(2, 3)
        uf.rollback(0)
        for i in range(4):
            self.assertEqual(uf.size(i), 1)


if __name__ == "__main__":
    unittest.main()
