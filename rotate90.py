def rotate90(grid):
    for _ in range(4):
        grid = [list(g) for g in zip(*grid[::-1])]
        yield grid


def transpose(grid):
    return [list(g) for g in zip(*grid)]
