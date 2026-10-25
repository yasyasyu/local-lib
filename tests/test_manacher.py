"""manacher.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from manacher import manacher, palindrome_lengths


def is_pal(t):
    return t == t[::-1]


def brute_radius(s):
    n = len(s)
    res = []
    for i in range(n):
        r = 1
        while i - r >= 0 and i + r < n and s[i - r] == s[i + r]:
            r += 1
        res.append(r)
    return res


def brute_lengths(s):
    n = len(s)
    res = []
    for k in range(2 * n - 1):
        best = 0
        for l in range(n):
            for r in range(l + 1, n + 1):
                if l + r - 1 == k and is_pal(s[l:r]):
                    best = max(best, r - l)
        res.append(best)
    return res


class TestManacher(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(manacher("abaaba"), [1, 2, 1, 1, 2, 1])
        L = palindrome_lengths("abba")
        self.assertEqual(L, [1, 0, 1, 4, 1, 0, 1])
        self.assertEqual(max(L), 4)
        self.assertTrue(L[0 + 4 - 1] >= 4)

    def test_empty(self):
        self.assertEqual(manacher(""), [])
        self.assertEqual(palindrome_lengths(""), [])

    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(300):
            s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 12)))
            self.assertEqual(manacher(s), brute_radius(s), s)
            self.assertEqual(palindrome_lengths(s), brute_lengths(s), s)

    def test_is_palindrome_query(self):
        rng = random.Random(1)
        for _ in range(100):
            s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 10)))
            L = palindrome_lengths(s)
            for l in range(len(s)):
                for r in range(l + 1, len(s) + 1):
                    self.assertEqual(L[l + r - 1] >= r - l, is_pal(s[l:r]))

    def test_list_input(self):
        self.assertEqual(palindrome_lengths([1, 2, 2, 1, 3]), [1, 0, 1, 4, 1, 0, 1, 0, 1])


if __name__ == "__main__":
    unittest.main()
