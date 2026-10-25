"""inversion_count.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from inversion_count import inversion_count


def brute(a):
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > a[j])


class TestInversionCount(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(inversion_count([3, 1, 2]), 2)
        self.assertEqual(inversion_count([1, 1, 1]), 0)

    def test_empty_and_single(self):
        self.assertEqual(inversion_count([]), 0)
        self.assertEqual(inversion_count([5]), 0)

    def test_reversed(self):
        n = 1000
        self.assertEqual(inversion_count(list(range(n, 0, -1))), n * (n - 1) // 2)

    def test_does_not_modify_input(self):
        a = [3, 1, 2]
        inversion_count(a)
        self.assertEqual(a, [3, 1, 2])

    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(300):
            a = [rng.randint(0, 5) for _ in range(rng.randint(0, 40))]
            self.assertEqual(inversion_count(a), brute(a))

    def test_large_values_and_strings(self):
        self.assertEqual(inversion_count([10**18, -(10**18), 0]), 2)
        self.assertEqual(inversion_count(["b", "a", "c"]), 1)


if __name__ == "__main__":
    unittest.main()
