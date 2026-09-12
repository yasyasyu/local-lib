"""add_treeview.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from add_treeview import add_tree_view


class _FakeSegtree:
    """セグメント木風の内部構造(_size, _d)を持つダミークラス"""

    def __init__(self, n):
        self._size = n
        self._d = [0] * (2 * n)


class TestAddTreeView(unittest.TestCase):
    def test_adds_str_method(self):
        add_tree_view(_FakeSegtree)
        self.assertTrue(hasattr(_FakeSegtree, "__str__"))

    def test_view_does_not_raise_and_returns_string(self):
        add_tree_view(_FakeSegtree)
        tree = _FakeSegtree(4)
        result = str(tree)
        self.assertIsInstance(result, str)
        self.assertIn("\n", result)


if __name__ == "__main__":
    unittest.main()
