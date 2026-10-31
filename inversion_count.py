from typing import Sequence, TypeVar

T = TypeVar("T")


def inversion_count(a: Sequence[T]) -> int:
    """転倒数（i < j かつ a[i] > a[j] となる組の個数）を返す。O(N log N)

    値は比較できれば何でもよい（座標圧縮は不要）。等しい値の組は数えない。
    マージソートをしながら、右側から取り出した要素について、左側に残っている個数を数える。
    バブルソートで隣を入れ替える回数の最小値と同じ。

    使い方::

        inversion_count([3, 1, 2])     # 2（(3, 1) と (3, 2)）
        inversion_count([1, 1, 1])     # 0

    https://github.com/yasyasyu/local-lib/blob/master/inversion_count.py
    """
    n = len(a)
    src = list(a)
    dst = src[:]
    count = 0
    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            i, j, k = lo, mid, lo
            while i < mid and j < hi:
                if src[j] < src[i]:
                    # src[i:mid] の要素はすべて src[j] より大きい
                    count += mid - i
                    dst[k] = src[j]
                    j += 1
                else:
                    dst[k] = src[i]
                    i += 1
                k += 1
            while i < mid:
                dst[k] = src[i]
                i += 1
                k += 1
            while j < hi:
                dst[k] = src[j]
                j += 1
                k += 1
        src, dst = dst, src
        width *= 2
    return count
