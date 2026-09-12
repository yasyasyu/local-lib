def compress(arr):
    """座標圧縮。値からその順位(0-indexed)への辞書を返す。

    使い方:
        compress([30, 10, 20])  # {10: 0, 20: 1, 30: 2}
    """
    return {v: i for i, v in enumerate(sorted(set(arr)))}
