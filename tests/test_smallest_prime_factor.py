"""smallest_prime_factor.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _math import Eratosthenes, divisors, prime_factorize
from smallest_prime_factor import SmallestPrimeFactor


class TestSmallestPrimeFactor(unittest.TestCase):
    def test_docstring_examples(self):
        spf = SmallestPrimeFactor(10**6)
        self.assertEqual(spf.factorize(360), {2: 3, 3: 2, 5: 1})
        self.assertTrue(spf.is_prime(97))
        self.assertEqual(spf.divisors(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(spf.spf[12], 2)

    def test_small_N(self):
        for N in range(0, 30):
            spf = SmallestPrimeFactor(N)
            self.assertEqual(len(spf.spf), N + 1)
            self.assertEqual([x for x in range(N + 1) if spf.is_prime(x)], Eratosthenes(N))

    def test_matches_trial_division(self):
        N = 20000
        spf = SmallestPrimeFactor(N)
        primes = set(Eratosthenes(N))
        for x in range(2, N + 1):
            self.assertEqual(spf.spf[x], min(p for p in prime_factorize(x)), x)
            self.assertEqual(spf.factorize(x), dict(sorted(prime_factorize(x).items())), x)
            self.assertEqual(spf.is_prime(x), x in primes)
        for x in range(1, 3000):
            self.assertEqual(spf.divisors(x), divisors(x), x)

    def test_one(self):
        spf = SmallestPrimeFactor(10)
        self.assertEqual(spf.factorize(1), {})
        self.assertEqual(spf.divisors(1), [1])
        self.assertFalse(spf.is_prime(1))
        self.assertFalse(spf.is_prime(0))


if __name__ == "__main__":
    unittest.main()
