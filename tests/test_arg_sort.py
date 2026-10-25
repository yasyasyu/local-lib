"""arg_sort.pyのテストコード

arg_sort.pyは `from .cmp_sort import sort_by_cmp` という相対インポートを
使っているため、パッケージとしてインポートする必要がある。
親ディレクトリをsys.pathに追加し、フォルダ名前空間パッケージ経由で読み込む。
"""

import importlib
import itertools
import math
import random
import sys
import unittest
from pathlib import Path

_LIB_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_LIB_DIR.parent))

_mod = importlib.import_module(f"{_LIB_DIR.name}.arg_sort")
arg_sort = _mod.arg_sort
arg_cmp = _mod.arg_cmp
make_arg_cmp = _mod.make_arg_cmp
sort_by_cmp = importlib.import_module(f"{_LIB_DIR.name}.cmp_sort").sort_by_cmp
lower_bound = importlib.import_module(f"{_LIB_DIR.name}.array_binary_search").lower_bound

# +x 方向から反時計回りに45度ずつ
EIGHT = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
GRID = [(x, y) for x in range(-3, 4) for y in range(-3, 4)]
STARTS = [(1, 0), (0, 1), (-1, 0), (0, -1), (2, 1), (-1, 3), (-2, -2), (3, -1)]


def sign(v):
    return (v > 0) - (v < 0)


def ref_key(p, start, closed):
    """atan2 で求めた、始線から反時計回りに測った偏角（小さい座標でのみ正確）。原点は -1"""
    if p == (0, 0):
        return -1.0
    g = math.gcd(*p)
    p = (p[0] // g, p[1] // g)
    gs = math.gcd(*start)
    s = (start[0] // gs, start[1] // gs)
    if p == s:
        return 0.0 if closed else 2 * math.pi
    # 同じ向きの点は約分して同じ入力にしてから atan2 を呼ぶので、値が完全に一致する
    return (math.atan2(p[1], p[0]) - math.atan2(s[1], s[0])) % (2 * math.pi)


class TestArgCmp(unittest.TestCase):
    def test_eight_directions(self):
        # 参考記事のテスト: 8方向の代表点の全組で、比較結果が添字の大小と一致する
        for i, j in itertools.product(range(8), repeat=2):
            self.assertEqual(sign(arg_cmp(EIGHT[i], EIGHT[j])), sign(i - j))

    def test_same_direction_is_equal(self):
        self.assertEqual(arg_cmp((1, 2), (3, 6)), 0)
        self.assertEqual(arg_cmp((-2, 0), (-5, 0)), 0)

    def test_origin_comes_first(self):
        for p in EIGHT:
            self.assertLess(arg_cmp((0, 0), p), 0)
            self.assertGreater(arg_cmp(p, (0, 0)), 0)
        self.assertEqual(arg_cmp((0, 0), (0, 0)), 0)

    def test_matches_reference_for_all_starts(self):
        # 全組で比較結果が参照と一致する（= 推移律を満たす全前順序になっている）
        for start in STARTS:
            for closed in (True, False):
                cmp = make_arg_cmp(start, closed)
                for p, q in itertools.product(GRID, repeat=2):
                    want = sign(ref_key(p, start, closed) - ref_key(q, start, closed))
                    self.assertEqual(sign(cmp(p, q)), want, (start, closed, p, q))

    def test_distinguishes_close_angles_with_large_coordinates(self):
        p, q = (10**9, 10**9 - 1), (10**9 - 1, 10**9 - 2)
        self.assertEqual(math.atan2(p[1], p[0]), math.atan2(q[1], q[0]))
        self.assertGreater(arg_cmp(p, q), 0)  # q の方が偏角が小さい

    def test_atan2_order(self):
        # start=(-1, 0), closed=False で atan2 の値域 (-π, π] の順になる
        pts = [p for p in GRID if p != (0, 0)]
        got = sort_by_cmp(pts, make_arg_cmp((-1, 0), closed=False))
        self.assertEqual(got, sorted(pts, key=lambda p: math.atan2(p[1], p[0])))


class TestArgSort(unittest.TestCase):
    def test_docstring_example(self):
        self.assertEqual(arg_sort([(0, -1), (-1, 0), (1, 1), (1, 0)]), [(1, 0), (1, 1), (-1, 0), (0, -1)])

    def test_eight_directions_shuffled(self):
        a = EIGHT[:]
        random.Random(0).shuffle(a)
        self.assertEqual(arg_sort(a), EIGHT)

    def test_empty(self):
        self.assertEqual(arg_sort([]), [])

    def test_does_not_modify_input(self):
        a = [(0, 1), (1, 0)]
        arg_sort(a)
        self.assertEqual(a, [(0, 1), (1, 0)])

    def test_closed_and_open(self):
        a = [(0, 1), (2, 0), (1, 1), (1, 0)]
        self.assertEqual(arg_sort(a), [(2, 0), (1, 0), (1, 1), (0, 1)])
        self.assertEqual(arg_sort(a, closed=False), [(1, 1), (0, 1), (2, 0), (1, 0)])

    def test_stable_and_distance_tiebreak(self):
        a = [(3, 3), (1, 0), (1, 1), (2, 2)]
        self.assertEqual(arg_sort(a), [(1, 0), (3, 3), (1, 1), (2, 2)])
        by_dist = sorted(a, key=lambda p: p[0] * p[0] + p[1] * p[1])
        self.assertEqual(arg_sort(by_dist), [(1, 0), (1, 1), (2, 2), (3, 3)])

    def test_matches_make_arg_cmp_random(self):
        rng = random.Random(1)
        for _ in range(200):
            start = rng.choice(STARTS)
            closed = rng.random() < 0.5
            pts = [(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(rng.randint(0, 30))]
            want = sort_by_cmp(pts, make_arg_cmp(start, closed))
            self.assertEqual(arg_sort(pts, start, closed), want)

    def test_large_coordinates(self):
        L = 10**9
        rng = random.Random(2)
        pts = [(rng.randint(-L, L), rng.randint(-L, L)) for _ in range(500)]
        a = arg_sort(pts)
        for p, q in zip(a, a[1:]):
            self.assertLessEqual(arg_cmp(p, q), 0)

    def test_count_in_angle_range_with_lower_bound(self):
        a = arg_sort(GRID)
        got = lower_bound(a, (-1, 1), arg_cmp) - lower_bound(a, (1, 1), arg_cmp)
        want = sum(1 for p in GRID if p != (0, 0) and math.pi / 4 <= ref_key(p, (1, 0), True) < 3 * math.pi / 4)
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
