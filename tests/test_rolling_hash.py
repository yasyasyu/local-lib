"""rolling_hash.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rolling_hash import RollingHash


class TestRollingHash(unittest.TestCase):
    def test_equal_substrings_have_equal_hash(self):
        rh = RollingHash("abcabc")
        self.assertEqual(rh.get(0, 3), rh.get(3, 6))

    def test_different_substrings_have_different_hash(self):
        rh = RollingHash("abcabd")
        self.assertNotEqual(rh.get(0, 3), rh.get(3, 6))

    def test_full_string_hash_matches_prefix(self):
        rh = RollingHash("hello")
        self.assertEqual(rh.get(0, 5), rh.hash[5])

    def test_lcp_of_identical_strings(self):
        rh = RollingHash("abcabc")
        self.assertEqual(rh.lcp(0, 3), 3)

    def test_lcp_partial_match(self):
        rh = RollingHash("abcabd")
        self.assertEqual(rh.lcp(0, 3), 2)

    def test_lcp_no_match(self):
        rh = RollingHash("abcxyz")
        self.assertEqual(rh.lcp(0, 3), 0)

    def test_matches_brute_force_randomized(self):
        random.seed(0)
        alphabet = "ab"
        for _ in range(20):
            s = "".join(random.choice(alphabet) for _ in range(30))
            rh = RollingHash(s, base=random.randint(37, 1000))
            for _ in range(20):
                l1 = random.randint(0, len(s) - 1)
                r1 = random.randint(l1 + 1, len(s))
                l2 = random.randint(0, len(s) - 1)
                r2 = random.randint(l2 + 1, len(s))
                expected = s[l1:r1] == s[l2:r2]
                actual = rh.get(l1, r1) == rh.get(l2, r2)
                self.assertEqual(actual, expected, (s, l1, r1, l2, r2))


if __name__ == "__main__":
    unittest.main()
