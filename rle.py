from itertools import groupby


def rle(S):
    S = groupby(S)
    ret = []
    for k, v in S:
        ret.append((k, len(list(v))))

    return ret
