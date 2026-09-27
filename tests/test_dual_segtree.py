"""dual_segtree.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dual_segtree import DualSegTree

MOD = 998244353


def assign_tree(v):
    """区間代入（Noneが恒等写像）"""
    return DualSegTree(
        lambda f, x: x if f is None else f,
        lambda f, g: g if f is None else f,
        None,
        v,
    )


def add_tree(v):
    """区間加算"""
    return DualSegTree(lambda f, x: f + x, lambda f, g: f + g, 0, v)


def affine_tree(v):
    """区間アフィン変換 x -> a*x + b（非可換な作用）"""
    return DualSegTree(
        lambda f, x: (f[0] * x + f[1]) % MOD,
        lambda f, g: (f[0] * g[0] % MOD, (f[0] * g[1] + f[1]) % MOD),
        (1, 0),
        v,
    )


class TestDualSegTree(unittest.TestCase):
    def test_docstring_example_assign(self):
        seg = assign_tree([0] * 5)
        seg.apply(1, 4, 7)
        self.assertEqual(seg.get_all(), [0, 7, 7, 7, 0])
        seg.apply(2, 9)
        self.assertEqual(seg.get(2), 9)
        seg.set(3, 1)
        self.assertEqual(seg.get_all(), [0, 7, 9, 1, 0])

    def test_docstring_example_add(self):
        seg = add_tree([1, 2, 3])
        seg.apply(0, 2, 10)
        self.assertEqual(seg.get_all(), [11, 12, 3])

    def test_empty_range_does_nothing(self):
        seg = add_tree([1, 2, 3])
        seg.apply(1, 1, 100)
        self.assertEqual(seg.get_all(), [1, 2, 3])

    def test_size_one(self):
        seg = assign_tree(["a"])
        seg.apply(0, 1, "b")
        self.assertEqual(seg.get(0), "b")
        seg.set(0, "c")
        seg.apply(0, 1, None)
        self.assertEqual(seg.get(0), "c")

    def test_set_is_not_overwritten_by_older_apply(self):
        # setの前に積まれていた作用が、set後の値に掛かってしまわないこと
        seg = assign_tree([0] * 8)
        seg.apply(0, 8, 5)
        seg.set(3, 1)
        self.assertEqual(seg.get_all(), [5, 5, 5, 1, 5, 5, 5, 5])

    def test_matches_brute_force_randomized(self):
        for make, gen_act, act in [
            (
                assign_tree,
                lambda: random.randint(0, 9),
                lambda f, x: f,
            ),
            (
                add_tree,
                lambda: random.randint(-5, 5),
                lambda f, x: f + x,
            ),
            (
                affine_tree,
                lambda: (random.randint(0, 5), random.randint(0, 5)),
                lambda f, x: (f[0] * x + f[1]) % MOD,
            ),
        ]:
            random.seed(0)
            for n in list(range(1, 10)) + [16, 17, 30]:
                arr = [random.randint(0, 9) for _ in range(n)]
                seg = make(list(arr))
                for _ in range(200):
                    r = random.random()
                    if r < 0.4:
                        left = random.randint(0, n)
                        right = random.randint(left, n)
                        f = gen_act()
                        for i in range(left, right):
                            arr[i] = act(f, arr[i])
                        seg.apply(left, right, f)
                    elif r < 0.55:
                        p = random.randint(0, n - 1)
                        f = gen_act()
                        arr[p] = act(f, arr[p])
                        seg.apply(p, f=f)
                    elif r < 0.7:
                        p = random.randint(0, n - 1)
                        x = random.randint(0, 9)
                        arr[p] = x
                        seg.set(p, x)
                    elif r < 0.95:
                        p = random.randint(0, n - 1)
                        self.assertEqual(seg.get(p), arr[p], (make.__name__, n, p))
                    else:
                        self.assertEqual(seg.get_all(), arr, (make.__name__, n))
                self.assertEqual(seg.get_all(), arr, (make.__name__, n))


if __name__ == "__main__":
    unittest.main()
