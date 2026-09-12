"""doubling.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from doubling import Doubling


class TestDoubling(unittest.TestCase):
    def test_matches_repeated_application(self):
        mapping = [1, 2, 0]  # 0->1->2->0 の巡回
        d = Doubling(3, 10, lambda x: mapping[x])
        for x in range(3):
            for k in range(10):
                expected = x
                for _ in range(k):
                    expected = mapping[expected]
                self.assertEqual(d.get(x, k), expected, (x, k))

    def test_zero_steps_is_identity(self):
        mapping = [1, 2, 0]
        d = Doubling(3, 5, lambda x: mapping[x])
        for x in range(3):
            self.assertEqual(d.get(x, 0), x)


if __name__ == "__main__":
    unittest.main()
