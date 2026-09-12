"""bit_partial_set.pyのテストコード"""

import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bit_partial_set import bit_partial_set


def run(n):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        bit_partial_set(n)
    return [int(line.split()[1]) for line in buf.getvalue().strip().splitlines()]


class TestBitPartialSet(unittest.TestCase):
    def test_enumerates_nonzero_submasks_descending(self):
        self.assertEqual(run(0b1011), [11, 10, 9, 8, 3, 2, 1])

    def test_excludes_empty_set(self):
        """空集合(0)を含めてはいけない、というdocstringの仕様の回帰テスト"""
        self.assertNotIn(0, run(0b1011))

    def test_single_bit(self):
        self.assertEqual(run(0b1), [1])


if __name__ == "__main__":
    unittest.main()
