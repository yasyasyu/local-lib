from itertools import groupby
from typing import Iterable, TypeVar

T = TypeVar("T")


def rle(S: Iterable[T]) -> list[tuple[T, int]]:
    """ランレングス圧縮。(値, 連続回数)のリストを返す。O(N)

    使い方::

        rle("aaabbc")  # [('a', 3), ('b', 2), ('c', 1)]

    https://github.com/yasyasyu/local-lib/blob/master/rle.py
    """
    ret = []
    for k, v in groupby(S):
        ret.append((k, len(list(v))))

    return ret
