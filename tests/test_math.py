"""_math.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _math import divisors, Eratosthenes, prime_factorize, section_prime_sieve


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


class TestDivisors(unittest.TestCase):
    def test_divisors_of_composite(self):
        self.assertEqual(sorted(divisors(12)), [1, 2, 3, 4, 6, 12])

    def test_divisors_of_prime(self):
        self.assertEqual(sorted(divisors(13)), [1, 13])

    def test_divisors_of_perfect_square(self):
        self.assertEqual(sorted(divisors(16)), [1, 2, 4, 8, 16])

    def test_divisors_of_one(self):
        self.assertEqual(divisors(1), [1])


class TestEratosthenes(unittest.TestCase):
    def test_matches_brute_force_for_various_n(self):
        """境界付近(sqrt(N)ちょうど)でふるいが抜けるバグの回帰テスト"""
        for n in [2, 3, 4, 9, 10, 25, 30, 100, 997, 1000]:
            expected = [p for p in range(2, n + 1) if is_prime(p)]
            self.assertEqual(sorted(Eratosthenes(n)), expected, f"n={n}")


class TestPrimeFactorize(unittest.TestCase):
    def test_factorize_composite(self):
        self.assertEqual(dict(prime_factorize(360)), {2: 3, 3: 2, 5: 1})

    def test_factorize_prime(self):
        self.assertEqual(dict(prime_factorize(17)), {17: 1})

    def test_factorize_one(self):
        self.assertEqual(dict(prime_factorize(1)), {})


class TestSectionPrimeSieve(unittest.TestCase):
    def test_matches_brute_force(self):
        """L以上最小の倍数の計算(--Lタイポ)の回帰テスト"""
        for L, R in [(1, 100), (2, 2), (10, 20), (14, 30), (10**6, 10**6 + 100)]:
            result = section_prime_sieve(L, R)
            expected = [is_prime(v) for v in range(L, R + 1)]
            self.assertEqual(result, expected, f"L={L}, R={R}")


if __name__ == "__main__":
    unittest.main()
