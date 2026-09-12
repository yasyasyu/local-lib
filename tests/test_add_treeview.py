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

    def test_returns_the_class_so_decorator_syntax_works(self):
        """@add_tree_view のように直接デコレータとして使っても、クラスがNoneにならないこと"""

        @add_tree_view
        class Decorated:
            def __init__(self, n):
                self._size = n
                self._d = [0] * (2 * n)

        self.assertIsNotNone(Decorated)
        self.assertEqual(Decorated.__name__, "Decorated")
        self.assertIsInstance(str(Decorated(4)), str)

    def test_return_value_equals_the_mutated_class(self):
        """add_tree_view(Cls) の戻り値をCls自身への再代入に使えること"""
        result = add_tree_view(_FakeSegtree)
        self.assertIs(result, _FakeSegtree)

    def test_view_does_not_raise_and_returns_string(self):
        add_tree_view(_FakeSegtree)
        tree = _FakeSegtree(4)
        result = str(tree)
        self.assertIsInstance(result, str)
        self.assertIn("\n", result)

    def test_columns_stay_aligned_when_values_have_different_widths(self):
        """値の桁数がバラバラでも、各行の幅が揃うこと（列がずれない）の回帰テスト"""
        tree = _FakeSegtree(4)
        # 葉に桁数の異なる値（3桁・負の数・大きな数）を混在させる
        tree._d = [0, 15, 3, 12, 1, 2, -1000000000, 100, 5]
        lines = str(tree).rstrip("\n").split("\n")
        self.assertEqual(len(lines), 3)
        widths = {len(line) for line in lines}
        self.assertEqual(len(widths), 1, lines)

    def test_matches_real_acl_segtree_layout(self):
        """ac-library-pythonのSegTreeにそのまま後付けしても、値・整列ともに壊れないこと"""
        from atcoder.segtree import SegTree

        add_tree_view(SegTree)
        seg = SegTree(op=lambda x, y: x + y, e=0, v=[100, 200, 300, 400, 500])
        lines = str(seg).rstrip("\n").split("\n")
        self.assertEqual(len(lines), 4)
        widths = {len(line) for line in lines}
        self.assertEqual(len(widths), 1, lines)
        # 一番下の行が葉の値そのものになっていること
        self.assertIn("0100", lines[-1])
        self.assertIn("0500", lines[-1])
        # 根の値が全要素の和になっていること
        self.assertIn("1500", lines[0])


if __name__ == "__main__":
    unittest.main()
