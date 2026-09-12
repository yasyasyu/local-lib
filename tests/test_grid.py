"""rotate90.py / grid_trim.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rotate90 import rotate90, transpose
from grid_trim import trim


class TestRotate90(unittest.TestCase):
    def test_single_90_degree_rotation(self):
        grid = [["a", "b"], ["c", "d"]]
        rotated = next(rotate90(grid))
        self.assertEqual(rotated, [["c", "a"], ["d", "b"]])

    def test_four_rotations_return_to_original(self):
        grid = [["a", "b"], ["c", "d"]]
        results = list(rotate90(grid))
        self.assertEqual(len(results), 4)
        self.assertEqual(results[-1], grid)

    def test_transpose(self):
        grid = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(transpose(grid), [[1, 4], [2, 5], [3, 6]])


class TestGridTrim(unittest.TestCase):
    def test_trims_blank_border(self):
        grid = [
            list("...."),
            list(".#.."),
            list("..#."),
            list("...."),
        ]
        result = trim(grid)
        self.assertEqual(result, [list("#."), list(".#")])

    def test_no_blank_border_is_unchanged(self):
        grid = [list("##"), list("##")]
        result = trim([row[:] for row in grid])
        self.assertEqual(result, grid)


if __name__ == "__main__":
    unittest.main()
