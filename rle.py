from itertools import groupby


def rle(S):
    """ランレングス圧縮。(値, 連続回数)のリストを返す。

    使い方:
        rle("aaabbc")  # [('a', 3), ('b', 2), ('c', 1)]
    """
    S = groupby(S)
    ret = []
    for k, v in S:
        ret.append((k, len(list(v))))

    return ret
