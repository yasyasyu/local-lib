"""_parser.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _parser import Parser


class TestParser(unittest.TestCase):
    def _eval(self, expr: str) -> int:
        return Parser().expr(expr)

    def test_addition(self):
        self.assertEqual(self._eval("1+2"), 3)

    def test_subtraction(self):
        self.assertEqual(self._eval("5-3"), 2)

    def test_multiplication_and_division(self):
        self.assertEqual(self._eval("2*3"), 6)
        self.assertEqual(self._eval("7/2"), 3)  # 整数除算(切り捨て)

    def test_operator_precedence(self):
        self.assertEqual(self._eval("2+3*4"), 14)

    def test_parentheses(self):
        self.assertEqual(self._eval("(2+3)*4"), 20)

    def test_implicit_multiplication_before_parenthesis(self):
        self.assertEqual(self._eval("2(3+4)"), 14)

    def test_negative_division_truncates_toward_zero(self):
        self.assertEqual(self._eval("0-7/2"), -3)


if __name__ == "__main__":
    unittest.main()
