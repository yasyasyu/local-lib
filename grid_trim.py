def trim(grid):
    """gridの周囲にある"#"を含まない余白の行・列を取り除く(gridは破壊的に変更される)。

    使い方:
        trim([list("...."), list(".#.."), list("..#."), list("....")])
        # [['#', '.'], ['.', '#']]

    https://github.com/yasyasyu/local-lib/blob/master/grid_trim.py
    """
    for _ in range(4):
        while True:
            if grid[-1].count("#") != 0:
                break
            grid.pop()
        grid = [list(x) for x in zip(*grid[::-1])]
    return grid
