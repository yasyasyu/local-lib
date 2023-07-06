def trim(grid):
    for _ in range(4):
        while True:
            if grid[-1].count("#") != 0:
                break
            grid.pop()
        grid = [list(x) for x in zip(*grid[::-1])]
    return grid
