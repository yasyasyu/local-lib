"""matrix_pow.pyのテストコード"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from matrix_pow import mat_mul, mat_pow


class TestMatMul(unittest.TestCase):
    def test_identity_multiplication(self):
        A = [[1, 2], [3, 4]]
        I = [[1, 0], [0, 1]]
        self.assertEqual(mat_mul(A, I), A)

    def test_basic_multiplication(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        self.assertEqual(mat_mul(A, B), [[19, 22], [43, 50]])

    def test_multiplication_with_mod(self):
        A = [[10, 0], [0, 10]]
        B = [[10, 0], [0, 10]]
        self.assertEqual(mat_mul(A, B, mod=7), [[2, 0], [0, 2]])


class TestMatPow(unittest.TestCase):
    def test_power_zero_is_identity(self):
        A = [[1, 2], [3, 4]]
        self.assertEqual(mat_pow(A, 0), [[1, 0], [0, 1]])

    def test_power_one_is_self(self):
        A = [[1, 2], [3, 4]]
        self.assertEqual(mat_pow(A, 1), A)

    def test_fibonacci_via_matrix_power(self):
        A = [[1, 1], [1, 0]]
        fibs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        for n in range(1, len(fibs)):
            self.assertEqual(mat_pow(A, n)[0][1], fibs[n])

    def test_matches_repeated_multiplication(self):
        A = [[2, 1], [1, 1]]
        expected = [[1, 0], [0, 1]]
        for _ in range(7):
            expected = mat_mul(expected, A)
        self.assertEqual(mat_pow(A, 7), expected)

    def test_power_with_mod(self):
        A = [[1, 1], [1, 0]]
        mod = 1000
        result = mat_pow(A, 50, mod=mod)
        expected = mat_pow(A, 50)
        for i in range(2):
            for j in range(2):
                self.assertEqual(result[i][j], expected[i][j] % mod)


if __name__ == "__main__":
    unittest.main()
