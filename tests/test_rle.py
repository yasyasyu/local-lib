"""rle.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rle import rle


class TestRle(unittest.TestCase):
    def test_basic_string(self):
        self.assertEqual(rle("aaabbc"), [("a", 3), ("b", 2), ("c", 1)])

    def test_no_repeats(self):
        self.assertEqual(rle("abc"), [("a", 1), ("b", 1), ("c", 1)])

    def test_empty(self):
        self.assertEqual(rle(""), [])

    def test_list_input(self):
        self.assertEqual(rle([1, 1, 2, 2, 2]), [(1, 2), (2, 3)])


if __name__ == "__main__":
    unittest.main()
