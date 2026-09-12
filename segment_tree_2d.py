from atcoder.segtree import SegTree


class SegmentTree2D:
    """2次元セグメント木（1点更新・矩形集約をO(log H log W)で処理する、任意のモノイド用）

    ac-library-pythonにセグ木の2次元版は無いため、加算以外（min/max/gcdなど）の
    矩形集約が必要なときに使う。単純な矩形和だけでよいなら`fenwick_tree_2d.py`の方が軽い。
    opは可換（足し算・min・max・gcd・xorなど）であることを前提にしている。

    内部では「行方向の外側セグ木の各ノードが、列方向の`atcoder.segtree.SegTree`を1つ持つ」
    構成にして、列方向の1次元セグ木ロジックは全てac-library-pythonに任せている。

    使い方:
        seg = SegmentTree2D(3, 3, op=min, e=float("inf"))
        seg.update(1, 1, 5)
        seg.update(0, 2, 3)
        seg.query(0, 0, 3, 3)  # 矩形[0,3)x[0,3)のmin -> 3
        seg.query(0, 0, 2, 2)  # 矩形[0,2)x[0,2)のmin -> 5
        seg.get(1, 1)          # (1, 1)の現在値 -> 5

        # 初期値を渡して一括構築する場合（O(HW)）
        seg2 = SegmentTree2D(3, 3, op=lambda a, b: a + b, e=0, v=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        seg2.query(0, 0, 3, 3)  # 45

    https://github.com/yasyasyu/local-lib/blob/master/segment_tree_2d.py
    """

    def __init__(self, h: int, w: int, op, e, v=None) -> None:
        self.h = h
        self.w = w
        self.op = op
        self.e = e

        self.size_h = 1
        while self.size_h < max(h, 1):
            self.size_h *= 2

        # tree[i]: 行方向の外側セグ木のノードiが担当する行範囲に対応する、列方向のSegTree
        self.tree = [None] * (2 * self.size_h)
        for x in range(self.size_h):
            row = v[x] if v is not None and x < h else [e] * w
            self.tree[x + self.size_h] = SegTree(op, e, list(row))

        for i in range(self.size_h - 1, 0, -1):
            left, right = self.tree[2 * i], self.tree[2 * i + 1]
            merged = [op(left.get(y), right.get(y)) for y in range(w)]
            self.tree[i] = SegTree(op, e, merged)

    def get(self, x: int, y: int):
        """座標(x, y)の現在値を返す。"""
        return self.tree[x + self.size_h].get(y)

    def update(self, x: int, y: int, val) -> None:
        """座標(x, y)の値をvalに更新する。"""
        i = x + self.size_h
        self.tree[i].set(y, val)
        i //= 2
        while i >= 1:
            left, right = self.tree[2 * i], self.tree[2 * i + 1]
            self.tree[i].set(y, self.op(left.get(y), right.get(y)))
            i //= 2

    def query(self, x1: int, y1: int, x2: int, y2: int):
        """半開矩形[x1, x2) x [y1, y2)の集約値を返す。"""
        l = x1 + self.size_h
        r = x2 + self.size_h
        res_l = self.e
        res_r = self.e
        while l < r:
            if l & 1:
                res_l = self.op(res_l, self.tree[l].prod(y1, y2))
                l += 1
            if r & 1:
                r -= 1
                res_r = self.op(self.tree[r].prod(y1, y2), res_r)
            l //= 2
            r //= 2
        return self.op(res_l, res_r)
