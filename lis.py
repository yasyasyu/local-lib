from bisect import bisect_left, bisect_right
from typing import Sequence, TypeVar

T = TypeVar("T")


def lis_ending_at(a: Sequence[T], strict: bool = True) -> list[int]:
    """各 i について、a[i] で終わる最長増加部分列の長さを返す。O(N log N)

    strict: True なら狭義単調増加（a[i] < a[j]）、False なら広義単調増加（a[i] <= a[j]）。
    LIS の長さは max(lis_ending_at(a))。逆順に並べた配列にも使えば、
    「a[i] を通る最長増加部分列の長さ」も求められる。

    使い方:
        lis_ending_at([3, 1, 4, 1, 5, 9, 2, 6])         # [1, 1, 2, 1, 3, 4, 2, 4]
        lis_ending_at([1, 1, 2], strict=False)          # [1, 2, 3]

        # a[i] を通る最長増加部分列の長さ（狭義）
        left = lis_ending_at(a)
        right = lis_ending_at([-x for x in reversed(a)])[::-1]  # a[i] から始まる長さ
        through = [l + r - 1 for l, r in zip(left, right)]

    https://github.com/yasyasyu/local-lib/blob/master/lis.py
    """
    find = bisect_left if strict else bisect_right
    tails: list[T] = []  # tails[k]: 長さ k + 1 の増加部分列の末尾として、ありうる最小の値
    res = []
    for x in a:
        k = find(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
        res.append(k + 1)
    return res


def lis(a: Sequence[T], strict: bool = True) -> list[int]:
    """最長増加部分列を1つ求め、その添字のリストを返す（値は [a[i] for i in lis(a)]）。O(N log N)

    strict: True なら狭義単調増加、False なら広義単調増加。
    長さだけでよいなら len(lis(a)) でも、max(lis_ending_at(a), default=0) でもよい。

    使い方:
        idx = lis([3, 1, 4, 1, 5, 9, 2, 6])  # [1, 2, 4, 7]（値は [1, 4, 5, 6]）
        len(idx)                             # 4

    https://github.com/yasyasyu/local-lib/blob/master/lis.py
    """
    find = bisect_left if strict else bisect_right
    tails: list[T] = []
    tails_idx: list[int] = []  # tails_idx[k]: tails[k] の値を持つ添字
    prev = [-1] * len(a)  # prev[i]: a[i] の1つ前に来る要素の添字
    for i, x in enumerate(a):
        k = find(tails, x)
        if k == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[k] = x
            tails_idx[k] = i
        if k > 0:
            prev[i] = tails_idx[k - 1]
    res = []
    i = tails_idx[-1] if tails_idx else -1
    while i != -1:
        res.append(i)
        i = prev[i]
    return res[::-1]
