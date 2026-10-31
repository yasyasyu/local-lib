from bisect import bisect_left, bisect_right
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")


def lower_bound(
    a: Sequence[T],
    x: T,
    cmp: Callable[[T, T], int] | None = None,
    lo: int = 0,
    hi: int | None = None,
) -> int:
    """ソート済み配列 a[lo:hi] で、x より前に来ない最初の要素の添字を返す（C++のlower_bound）。O(log N) 回 cmp を呼ぶ

    :param cmp: a のソートに使った比較関数（cmp_sort.sort_by_cmp と同じ約束）。
        省略すると < で比較する（bisect.bisect_left と同じ）。

    該当する要素がなければ hi を返す。

    使い方::

        lower_bound([1, 3, 3, 5], 3)  # 1
        lower_bound([1, 3, 3, 5], 4)  # 3

        # 降順の配列
        lower_bound([5, 3, 3, 1], 3, lambda x, y: y - x)  # 1

    https://github.com/yasyasyu/local-lib/blob/master/array_binary_search.py
    """
    if hi is None:
        hi = len(a)
    if cmp is None:
        return bisect_left(a, x, lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if cmp(a[mid], x) < 0:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(
    a: Sequence[T],
    x: T,
    cmp: Callable[[T, T], int] | None = None,
    lo: int = 0,
    hi: int | None = None,
) -> int:
    """ソート済み配列 a[lo:hi] で、x より後ろに来る最初の要素の添字を返す（C++のupper_bound）。O(log N) 回 cmp を呼ぶ

    :param cmp: a のソートに使った比較関数（cmp_sort.sort_by_cmp と同じ約束）。
        省略すると < で比較する（bisect.bisect_right と同じ）。

    該当する要素がなければ hi を返す。
    upper_bound(a, x) - lower_bound(a, x) が x と等しい要素の個数になる。

    使い方::

        upper_bound([1, 3, 3, 5], 3)  # 3
        upper_bound([1, 3, 3, 5], 0)  # 0

    https://github.com/yasyasyu/local-lib/blob/master/array_binary_search.py
    """
    if hi is None:
        hi = len(a)
    if cmp is None:
        return bisect_right(a, x, lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if cmp(x, a[mid]) < 0:
            hi = mid
        else:
            lo = mid + 1
    return lo


def partition_point(
    a: Sequence[T],
    pred: Callable[[T], bool],
    lo: int = 0,
    hi: int | None = None,
) -> int:
    """a[lo:hi] で pred が False になる最初の添字を返す（C++のpartition_point）。O(log N) 回 pred を呼ぶ

    pred は a[lo:hi] の前半で True、後半で False になっていること。
    すべて True なら hi、すべて False なら lo を返す（= pred が True の要素の個数 + lo）。

    使い方::

        a = [1, 3, 3, 5, 8]
        partition_point(a, lambda v: v * v < 20)  # 3（5 * 5 >= 20）

        # 1つ目の要素が1未満の範囲の長さ
        b = [(0, 1), (0, 4), (1, 2), (1, 9)]
        partition_point(b, lambda p: p[0] < 1)  # 2

    https://github.com/yasyasyu/local-lib/blob/master/array_binary_search.py
    """
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(a[mid]):
            lo = mid + 1
        else:
            hi = mid
    return lo
