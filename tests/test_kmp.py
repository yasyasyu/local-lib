"""kmp.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kmp import kmp_search, prefix_function


def brute_pi(s):
    res = []
    for i in range(len(s)):
        t = s[: i + 1]
        best = 0
        for k in range(1, len(t)):
            if t[:k] == t[-k:]:
                best = k
        res.append(best)
    return res


def brute_search(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text[i : i + len(pattern)] == pattern]


def brute_period(s):
    for p in range(1, len(s) + 1):
        if all(s[i] == s[i - p] for i in range(p, len(s))):
            return p


class TestKmp(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(prefix_function("abacaba"), [0, 0, 1, 0, 1, 2, 3])
        s = "abcabcab"
        self.assertEqual(len(s) - prefix_function(s)[-1], 3)
        self.assertEqual(kmp_search("abababa", "aba"), [0, 2, 4])
        self.assertEqual(kmp_search("abc", "d"), [])

    def test_empty(self):
        self.assertEqual(prefix_function(""), [])
        self.assertEqual(kmp_search("", "a"), [])
        self.assertEqual(kmp_search("ab", ""), [0, 1, 2])

    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(500):
            s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 15)))
            self.assertEqual(prefix_function(s), brute_pi(s))
            self.assertEqual(len(s) - prefix_function(s)[-1], brute_period(s))
            p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
            self.assertEqual(kmp_search(s, p), brute_search(s, p))

    def test_list_input(self):
        self.assertEqual(kmp_search([1, 2, 1, 2, 1], [1, 2, 1]), [0, 2])


if __name__ == "__main__":
    unittest.main()
