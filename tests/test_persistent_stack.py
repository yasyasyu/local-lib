"""persistent_stack.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from persistent_stack import PersistentStack


class TestPersistentStack(unittest.TestCase):
    def test_push_and_str(self):
        a = PersistentStack()
        a = a.push(1)
        a = a.push(2)
        self.assertEqual(str(a), "[1, 2]")
        self.assertEqual(a.peek(), 2)

    def test_pop_returns_previous_state(self):
        a = PersistentStack()
        a = a.push(1).push(2)
        b = a.pop()
        self.assertEqual(str(b), "[1]")
        self.assertEqual(str(a), "[1, 2]")  # 元のスタックは変更されない

    def test_pop_on_empty_is_noop(self):
        a = PersistentStack()
        self.assertEqual(str(a.pop()), "[]")

    def test_from_iterable(self):
        a = PersistentStack.from_iterable([1, 2, 3])
        self.assertEqual(str(a), "[1, 2, 3]")

    def test_iteration_with_falsy_values(self):
        """0や空文字などfalsyな値をpushしても反復が途切れないこと(__iter__のバグ回帰テスト)"""
        a = PersistentStack()
        a = a.push(1).push(0).push(2)
        self.assertEqual(list(a), [1, 0, 2])
        a = a.push("")
        self.assertEqual(list(a), [1, 0, 2, ""])

    def test_persistence_across_branches(self):
        """save1の状態を保存した後に片方だけpushしても、保存した状態は変化しない"""
        a = PersistentStack()
        a = a.push("a")
        save1 = a
        a = a.push("b")
        self.assertEqual(str(a), "[a, b]")
        self.assertEqual(str(save1), "[a]")


if __name__ == "__main__":
    unittest.main()
