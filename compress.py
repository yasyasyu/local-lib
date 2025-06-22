def compress(arr):
    return {v: i for i, v in enumerate(sorted(set(arr)))}
