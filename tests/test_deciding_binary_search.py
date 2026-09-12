"""deciding_binary_search.pyのテストコード

is_ok は `mid > 0` にハードコードされたテンプレートである
(問題ごとに書き換えて使うスニペット)。ここではテンプレートの
ループ構造そのものが壊れていないことを確認する。
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from deciding_binary_search import binary_search


class TestDecidingBinarySearch(unittest.TestCase):
    def test_finds_boundary_between_0_and_1(self):
        self.assertEqual(binary_search(-1, 10), 1)

    def test_ok_already_adjacent_to_ng(self):
        self.assertEqual(binary_search(0, 1), 1)

    def test_wide_range(self):
        self.assertEqual(binary_search(-1000, 1000), 1)


if __name__ == "__main__":
    unittest.main()
