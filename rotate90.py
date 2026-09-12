def rotate90(grid):
    """gridを90度ずつ回転したものを4回分(360度分)順に返すジェネレータ。

    使い方:
        for rotated in rotate90(grid):
            ...  # 90, 180, 270, 360(元と同じ)度回転したgridが順に得られる

    https://github.com/yasyasyu/local-lib/blob/master/rotate90.py
    """
    for _ in range(4):
        grid = [list(g) for g in zip(*grid[::-1])]
        yield grid


def transpose(grid):
    """gridを転置する。

    使い方:
        transpose([[1, 2, 3], [4, 5, 6]])  # [[1, 4], [2, 5], [3, 6]]

    https://github.com/yasyasyu/local-lib/blob/master/rotate90.py
    """
    return [list(g) for g in zip(*grid)]
