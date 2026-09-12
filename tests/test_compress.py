"""compress.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from compress import compress


class TestCompress(unittest.TestCase):
    def test_assigns_rank_by_sorted_order(self):
        self.assertEqual(compress([30, 10, 20]), {10: 0, 20: 1, 30: 2})

    def test_duplicates_share_rank(self):
        self.assertEqual(compress([5, 1, 5, 2]), {1: 0, 2: 1, 5: 2})

    def test_empty(self):
        self.assertEqual(compress([]), {})


if __name__ == "__main__":
    unittest.main()
