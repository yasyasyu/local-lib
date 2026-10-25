"""pollard_rho.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _math import Eratosthenes, prime_factorize
from pollard_rho import factorize, is_prime


def trial_is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


class TestIsPrime(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertTrue(is_prime(998244353))
        self.assertTrue(is_prime(10**18 + 9))
        self.assertFalse(is_prime(561))

    def test_matches_sieve(self):
        N = 100000
        primes = set(Eratosthenes(N))
        for n in range(-5, N + 1):
            self.assertEqual(is_prime(n), n in primes, n)

    def test_strong_pseudoprimes(self):
        # 小さい底で素数と誤判定されやすい合成数
        for n in [2047, 1373653, 25326001, 3215031751, 2152302898747, 3474749660383, 341550071728321, 3825123056546413051]:
            self.assertFalse(is_prime(n), n)

    def test_random_against_trial_division(self):
        rng = random.Random(0)
        for _ in range(300):
            n = rng.randint(10**9, 10**9 + 10**6)
            self.assertEqual(is_prime(n), trial_is_prime(n), n)


class TestFactorize(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(factorize(360), {2: 3, 3: 2, 5: 1})
        self.assertEqual(factorize(999999999999999989 * 2), {2: 1, 999999999999999989: 1})
        self.assertEqual(factorize(1), {})

    def test_matches_trial_division(self):
        rng = random.Random(1)
        for n in list(range(1, 2000)) + [rng.randint(1, 10**10) for _ in range(300)]:
            self.assertEqual(factorize(n), dict(sorted(prime_factorize(n).items())), n)

    def test_semiprimes_and_powers(self):
        rng = random.Random(2)
        big = [p for p in range(10**9, 10**9 + 2000) if trial_is_prime(p)]
        mid = [p for p in range(10**6, 10**6 + 2000) if trial_is_prime(p)]
        for _ in range(30):
            p, q = rng.sample(big, 2)
            self.assertEqual(factorize(p * q), dict(sorted({p: 1, q: 1}.items())))
            r = rng.choice(mid)
            self.assertEqual(factorize(r**3), {r: 3})
            self.assertEqual(factorize(p * p), {p: 2})
            self.assertEqual(factorize(2**5 * 3 * r * p), dict(sorted({2: 5, 3: 1, r: 1, p: 1}.items())))

    def test_random_large_numbers(self):
        rng = random.Random(3)
        for _ in range(50):
            n = rng.randint(1, 10**18)
            f = factorize(n)
            prod = 1
            for p, e in f.items():
                self.assertTrue(is_prime(p))
                prod *= p**e
            self.assertEqual(prod, n)
            self.assertEqual(list(f), sorted(f))


if __name__ == "__main__":
    unittest.main()
