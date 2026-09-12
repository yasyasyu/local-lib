from atcoder.fenwicktree import FenwickTree


class FenwickTree2D:
    """2次元Fenwick Tree（BIT）。点更新・矩形和取得をO(log H log W)で処理する。

    内部では「行方向の外側BITの各ノードが、列方向の`atcoder.fenwicktree.FenwickTree`を
    1つ持つ」構成にして、列方向の1次元BITロジックは全てac-library-pythonに任せている。

    使い方:
        bit = FenwickTree2D(5, 5)
        bit.add(1, 2, 3)     # (1, 2) に3を加算
        bit.add(3, 3, 4)     # (3, 3) に4を加算
        bit.sum(0, 0, 4, 4)  # 矩形[0,4)x[0,4)の和 -> 7
        bit.sum(0, 0, 2, 3)  # 矩形[0,2)x[0,3)の和 -> 3

    https://github.com/yasyasyu/local-lib/blob/master/fenwick_tree_2d.py
    """

    def __init__(self, h: int, w: int) -> None:
        self.h = h
        self.w = w
        # tree[i]: 行方向の外側BITのノードiが担当する行の集合について、列方向を管理するBIT
        self.tree = [FenwickTree(w) for _ in range(h + 1)]

    def add(self, x: int, y: int, val) -> None:
        """座標(x, y)にvalを加算する。"""
        i = x + 1
        while i <= self.h:
            self.tree[i].add(y, val)
            i += i & (-i)

    def _prefix_sum(self, x: int, y: int):
        """半開矩形[0, x) x [0, y)の和を返す。"""
        s = 0
        i = x
        while i > 0:
            s += self.tree[i].sum(0, y)
            i -= i & (-i)
        return s

    def sum(self, x1: int, y1: int, x2: int, y2: int):
        """半開矩形[x1, x2) x [y1, y2)の和を返す。"""
        return (
            self._prefix_sum(x2, y2)
            - self._prefix_sum(x1, y2)
            - self._prefix_sum(x2, y1)
            + self._prefix_sum(x1, y1)
        )
