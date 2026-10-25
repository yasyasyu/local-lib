from bisect import bisect_left
from typing import Sequence


class WaveletMatrix:
    """ウェーブレット行列。変更のない整数列について、区間の k 番目の値や値の範囲の個数を求める

    値は内部で座標圧縮するので、負の数や大きな数でもよい（σ は値の種類数）。
    構築 O(N log σ)、各クエリ O(log σ)。区間はすべて半開区間 [l, r)。

    使い方:
        wm = WaveletMatrix([5, 1, 4, 1, 5, 9, 2, 6])
        wm.kth_smallest(1, 6, 0)       # 1（a[1:6] = [1, 4, 1, 5, 9] で 0 番目に小さい値）
        wm.kth_smallest(1, 6, 2)       # 4
        wm.kth_largest(1, 6, 0)        # 9
        wm.range_freq(0, 8, 2, 6)      # 4（2 以上 6 未満の値 5, 4, 5, 2 の個数）
        wm.count(0, 8, 5)              # 2（値 5 の個数）
        wm.prev_value(0, 8, 5)         # 4（5 未満で最大の値）
        wm.next_value(0, 8, 7)         # 9（7 以上で最小の値）

    https://github.com/yasyasyu/local-lib/blob/master/wavelet_matrix.py
    """

    def __init__(self, a: Sequence[int]) -> None:
        """整数列 a から構築する。O(N log σ)"""
        self.n = len(a)
        self.vals = sorted(set(a))  # 圧縮後の値 c は、元の値 vals[c]
        cur = [bisect_left(self.vals, x) for x in a]
        self.bits = max(1, (len(self.vals) - 1).bit_length())
        # 上の桁から順に、各段で「その桁が0の要素を前、1の要素を後ろ」に安定に並べ替える
        # zeros[level][i]: その段の列の先頭 i 個のうち、桁が0の要素の個数
        self.zeros: list[list[int]] = [[] for _ in range(self.bits)]
        self.zero_total = [0] * self.bits
        for level in range(self.bits - 1, -1, -1):
            z = [0] * (self.n + 1)
            cnt = 0
            for i, c in enumerate(cur):
                if not (c >> level) & 1:
                    cnt += 1
                z[i + 1] = cnt
            self.zeros[level] = z
            self.zero_total[level] = cnt
            cur = [c for c in cur if not (c >> level) & 1] + [c for c in cur if (c >> level) & 1]

    def _count_less_code(self, l: int, r: int, code: int) -> int:
        """[l, r) のうち、圧縮後の値が code 未満の要素の個数。O(log σ)"""
        if code >= 1 << self.bits:
            return r - l
        res = 0
        for level in range(self.bits - 1, -1, -1):
            z = self.zeros[level]
            l0 = z[l]
            r0 = z[r]
            if (code >> level) & 1:
                res += r0 - l0
                zt = self.zero_total[level]
                l = zt + l - l0
                r = zt + r - r0
            else:
                l = l0
                r = r0
        return res

    def range_freq(self, l: int, r: int, lower: int, upper: int) -> int:
        """a[l:r] のうち、lower <= 値 < upper の要素の個数を返す。O(log σ)"""
        if lower >= upper:
            return 0
        return self._count_less_code(l, r, bisect_left(self.vals, upper)) - self._count_less_code(
            l, r, bisect_left(self.vals, lower)
        )

    def count(self, l: int, r: int, x: int) -> int:
        """a[l:r] の中の値 x の個数を返す。O(log σ)"""
        return self.range_freq(l, r, x, x + 1)

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        """a[l:r] の中で k 番目（0-indexed）に小さい値を返す。0 <= k < r - l であること。O(log σ)"""
        code = 0
        for level in range(self.bits - 1, -1, -1):
            z = self.zeros[level]
            l0 = z[l]
            r0 = z[r]
            if k < r0 - l0:
                l = l0
                r = r0
            else:
                k -= r0 - l0
                code |= 1 << level
                zt = self.zero_total[level]
                l = zt + l - l0
                r = zt + r - r0
        return self.vals[code]

    def kth_largest(self, l: int, r: int, k: int) -> int:
        """a[l:r] の中で k 番目（0-indexed）に大きい値を返す。0 <= k < r - l であること。O(log σ)"""
        return self.kth_smallest(l, r, r - l - 1 - k)

    def prev_value(self, l: int, r: int, upper: int) -> int | None:
        """a[l:r] の中で upper 未満の最大の値を返す（無ければ None）。O(log σ)"""
        cnt = self._count_less_code(l, r, bisect_left(self.vals, upper))
        return self.kth_smallest(l, r, cnt - 1) if cnt else None

    def next_value(self, l: int, r: int, lower: int) -> int | None:
        """a[l:r] の中で lower 以上の最小の値を返す（無ければ None）。O(log σ)"""
        cnt = self._count_less_code(l, r, bisect_left(self.vals, lower))
        return self.kth_smallest(l, r, cnt) if cnt < r - l else None

    def access(self, i: int) -> int:
        """a[i] を返す。O(log σ)"""
        code = 0
        for level in range(self.bits - 1, -1, -1):
            z = self.zeros[level]
            if z[i + 1] - z[i]:
                i = z[i]
            else:
                code |= 1 << level
                i = self.zero_total[level] + i - z[i]
        return self.vals[code]
