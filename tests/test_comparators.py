"""comparators.pyのテストコード"""

import itertools
import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cmp_sort import sort_by_cmp
from comparators import (
    check_cmp,
    concat_cmp,
    exchange_cmp,
    frac_cmp,
    key_cmp,
    reverse_cmp,
    then_cmp,
)


def sign(v):
    return (v > 0) - (v < 0)


def ref_value(p):
    """分数 (a, b) の参照値。分母0は ±∞"""
    a, b = p
    if b == 0:
        return float("inf") if a > 0 else float("-inf")
    return Fraction(a, b)


class TestFracCmp(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertLess(frac_cmp((1, 3), (1, 2)), 0)
        self.assertEqual(frac_cmp((1, 2), (2, 4)), 0)

    def test_negative_denominator(self):
        self.assertEqual(frac_cmp((1, -2), (-1, 2)), 0)
        self.assertLess(frac_cmp((1, -2), (1, 3)), 0)
        self.assertGreater(frac_cmp((-3, -4), (1, 2)), 0)

    def test_infinity(self):
        self.assertGreater(frac_cmp((1, 0), (10**18, 1)), 0)
        self.assertLess(frac_cmp((-1, 0), (-(10**18), 1)), 0)
        self.assertLess(frac_cmp((-1, 0), (1, 0)), 0)
        self.assertEqual(frac_cmp((2, 0), (1, 0)), 0)
        self.assertEqual(frac_cmp((-5, 0), (-1, 0)), 0)

    def test_matches_fraction_and_is_valid_order(self):
        vals = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if (a, b) != (0, 0)]
        for p, q in itertools.product(vals, repeat=2):
            want = ref_value(p) - ref_value(q) if ref_value(p) != ref_value(q) else 0
            self.assertEqual(sign(frac_cmp(p, q)), sign(want), (p, q))
        self.assertIsNone(check_cmp(vals, frac_cmp))

    def test_close_values_where_float_fails(self):
        p = (999999999, 1999999999)
        q = (999999998, 1999999997)
        self.assertEqual(p[0] / p[1], q[0] / q[1])  # 浮動小数点では区別できない
        self.assertEqual(sign(frac_cmp(p, q)), sign(Fraction(*p) - Fraction(*q)))
        self.assertNotEqual(frac_cmp(p, q), 0)

    def test_abc308c_sample(self):
        # 成功率 A/(A+B) の高い順、同率は番号の小さい順
        A = [1, 3, 2]
        B = [3, 1, 2]
        order = sort_by_cmp(range(3), reverse_cmp(key_cmp(lambda i: (A[i], A[i] + B[i]), frac_cmp)))
        self.assertEqual([i + 1 for i in order], [2, 3, 1])

    def test_abc308c_tie_keeps_index_order(self):
        A = [1, 2, 1]
        B = [1, 2, 3]
        order = sort_by_cmp(range(3), reverse_cmp(key_cmp(lambda i: (A[i], A[i] + B[i]), frac_cmp)))
        self.assertEqual(order, [0, 1, 2])


class TestConcatCmp(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual("".join(sort_by_cmp(["3", "30", "34"], concat_cmp)), "30334")
        self.assertEqual("".join(sort_by_cmp(["3", "30", "34"], reverse_cmp(concat_cmp))), "34330")

    def test_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(200):
            words = ["".join(rng.choice("012") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(1, 5))]
            all_concat = ["".join(p) for p in itertools.permutations(words)]
            self.assertEqual("".join(sort_by_cmp(words, concat_cmp)), min(all_concat))
            self.assertEqual("".join(sort_by_cmp(words, reverse_cmp(concat_cmp))), max(all_concat))

    def test_is_valid_order(self):
        words = ["".join(t) for n in range(1, 4) for t in itertools.product("01", repeat=n)]
        self.assertIsNone(check_cmp(words, concat_cmp))


class TestExchangeCmp(unittest.TestCase):
    @staticmethod
    def weighted_completion(tasks):
        t = 0
        total = 0
        for p, w in tasks:
            t += p
            total += w * t
        return total

    def test_docstring_example(self):
        tasks = [(3, 1), (1, 2), (2, 2)]
        cost = lambda a, b: a[1] * a[0] + b[1] * (a[0] + b[0])
        self.assertEqual(sort_by_cmp(tasks, exchange_cmp(cost)), [(1, 2), (2, 2), (3, 1)])

    def test_weighted_completion_matches_brute_force(self):
        cost = lambda a, b: a[1] * a[0] + b[1] * (a[0] + b[0])
        cmp = exchange_cmp(cost)
        rng = random.Random(1)
        for _ in range(200):
            tasks = [(rng.randint(1, 5), rng.randint(1, 5)) for _ in range(rng.randint(1, 6))]
            got = self.weighted_completion(sort_by_cmp(tasks, cmp))
            want = min(self.weighted_completion(p) for p in itertools.permutations(tasks))
            self.assertEqual(got, want)
            self.assertIsNone(check_cmp(tasks, cmp))


class TestCombinators(unittest.TestCase):
    def test_key_cmp_natural(self):
        cmp = key_cmp(len)
        self.assertLess(cmp("a", "bb"), 0)
        self.assertEqual(cmp("ab", "cd"), 0)

    def test_key_cmp_with_cmp(self):
        P = [(1, 2), (1, 3), (2, 3)]
        self.assertEqual(sort_by_cmp(range(3), key_cmp(lambda i: P[i], frac_cmp)), [1, 0, 2])

    def test_reverse_cmp(self):
        self.assertEqual(sort_by_cmp([3, 1, 2], reverse_cmp(key_cmp(lambda v: v))), [3, 2, 1])

    def test_then_cmp_matches_tuple_key(self):
        rng = random.Random(2)
        a = [(rng.randint(0, 3), rng.randint(0, 3), i) for i in range(50)]
        cmp = then_cmp(key_cmp(lambda t: t[0]), reverse_cmp(key_cmp(lambda t: t[1])))
        self.assertEqual(sort_by_cmp(a, cmp), sorted(a, key=lambda t: (t[0], -t[1])))

    def test_then_cmp_empty_is_all_equal(self):
        self.assertEqual(then_cmp()(1, 2), 0)


class TestCheckCmp(unittest.TestCase):
    def test_valid(self):
        self.assertIsNone(check_cmp([3, 1, 2, 2], lambda x, y: x - y))
        self.assertIsNone(check_cmp([], lambda x, y: x - y))

    def test_not_reflexive(self):
        self.assertEqual(check_cmp([1, 2], lambda x, y: -1), (1,))

    def test_not_antisymmetric(self):
        cmp = lambda x, y: 0 if x == y else -1  # 常に左が前
        self.assertEqual(check_cmp([1, 2], cmp), (1, 2))

    def test_not_transitive(self):
        # じゃんけん: 0 < 1 < 2 < 0
        cmp = lambda x, y: 0 if x == y else (-1 if (y - x) % 3 == 1 else 1)
        self.assertEqual(len(check_cmp([0, 1, 2], cmp)), 3)

    def test_cross_product_alone_is_not_an_order(self):
        # 偏角ソートの落とし穴: 半平面に分けずに外積だけで比べると一周で順序が壊れる
        eight = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        cross_only = lambda p, q: p[1] * q[0] - p[0] * q[1]
        self.assertIsNotNone(check_cmp(eight, cross_only))


if __name__ == "__main__":
    unittest.main()
