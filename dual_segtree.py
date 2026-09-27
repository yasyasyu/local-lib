import typing

# DualSegTree.applyで引数が省略されたことを表す値（Noneは作用として使われうるため別に用意する）
_NO_ARG = object()


class DualSegTree:
    """双対セグメント木（区間作用・1点取得をO(log N)で処理する）

    ac-library-pythonの`LazySegTree`から「区間の集約値（op, e, prod）」を取り除いたもの。
    区間更新して1点を読むだけの問題（区間代入・区間加算・区間chminなど）で、
    `LazySegTree`に意味のないop/eを渡す代わりに使う。区間の集約値が必要なら`LazySegTree`を使うこと。

    ノードには作用だけを持ち、葉にだけ値を持つ。1点取得・1点更新の前に根から葉までの
    作用を下へ流す（push）ので、作用が可換でなくても（区間代入・アフィン変換など）正しく動く。

    引数・メソッド名は`atcoder.lazysegtree.LazySegTree`に合わせている:
        mapping(f, x):     作用fを値xに適用した結果
        composition(f, g): gを適用した後にfを適用する作用（f∘g。fが新しい作用）
        id_:               恒等写像（何もしない作用）
        v:                 初期値のリスト

    計算量（mapping・compositionの1回の呼び出しをO(1)とした場合）:
        構築 O(N)、get / set / apply（1点・区間とも） O(log N)、get_all O(N)
        mapping・compositionが重い場合（行列など）は、その計算量が掛け算で効く。

    使い方:
        # 区間代入（Noneを「何もしない」とする）
        seg = DualSegTree(
            lambda f, x: x if f is None else f,
            lambda f, g: g if f is None else f,
            None,
            [0] * 5,
        )
        seg.apply(1, 4, 7)  # [1, 4)を7に -> [0, 7, 7, 7, 0]
        seg.apply(2, 9)     # 1点だけに作用させる -> [0, 7, 9, 7, 0]
        seg.get(2)          # 9
        seg.set(3, 1)       # -> [0, 7, 9, 1, 0]
        seg.get_all()       # [0, 7, 9, 1, 0]

        # 区間加算
        seg2 = DualSegTree(lambda f, x: f + x, lambda f, g: f + g, 0, [1, 2, 3])
        seg2.apply(0, 2, 10)
        seg2.get_all()      # [11, 12, 3]

    https://github.com/yasyasyu/local-lib/blob/master/dual_segtree.py
    """

    def __init__(
        self,
        mapping: typing.Callable[[typing.Any, typing.Any], typing.Any],
        composition: typing.Callable[[typing.Any, typing.Any], typing.Any],
        id_: typing.Any,
        v: typing.List[typing.Any],
    ) -> None:
        """初期値vで構築する。O(N)"""
        self._mapping = mapping
        self._composition = composition
        self._id = id_

        self._n = len(v)
        self._log = 0
        while (1 << self._log) < self._n:
            self._log += 1
        self._size = 1 << self._log
        # _d: 葉の値（要素ごと）、_lz: 内部ノードの未伝播の作用
        self._d = list(v)
        self._lz = [id_] * self._size

    def set(self, p: int, x: typing.Any) -> None:
        """p番目の値をxにする。O(log N)"""
        assert 0 <= p < self._n

        self._push_path(p)
        self._d[p] = x

    def get(self, p: int) -> typing.Any:
        """p番目の現在値を返す。O(log N)"""
        assert 0 <= p < self._n

        self._push_path(p)
        return self._d[p]

    def get_all(self) -> typing.List[typing.Any]:
        """全要素の現在値をリストで返す。O(N)"""
        for k in range(1, self._size):
            self._push(k)
        return list(self._d)

    def apply(self, left: int, right: typing.Any = _NO_ARG, f: typing.Any = _NO_ARG) -> None:
        """apply(left, right, f)で区間[left, right)に、apply(p, f)でp番目に作用fを適用する。O(log N)

        LazySegTreeと同じapply(p, f=f)の形でも1点に適用できる。
        恒等写像にNoneを使う場合もあるので、引数の省略はNoneではなく_NO_ARGで判定している。
        """
        if f is _NO_ARG:
            # apply(p, f)
            assert right is not _NO_ARG
            p, f = left, right
            right = None
        elif right is _NO_ARG:
            # apply(p, f=f)
            p = left
            right = None

        if right is None:
            assert 0 <= p < self._n

            self._push_path(p)
            self._d[p] = self._mapping(f, self._d[p])
            return

        assert 0 <= left <= right <= self._n
        if left == right:
            return

        left += self._size
        right += self._size

        # 区間の境界にかかるノードの古い作用を先に流しておく
        # （新しい作用fが、境界の外側にある古い作用より先に適用されてしまうのを防ぐ）
        for i in range(self._log, 0, -1):
            if ((left >> i) << i) != left:
                self._push(left >> i)
            if ((right >> i) << i) != right:
                self._push((right - 1) >> i)

        while left < right:
            if left & 1:
                self._all_apply(left, f)
                left += 1
            if right & 1:
                right -= 1
                self._all_apply(right, f)
            left >>= 1
            right >>= 1

    def _push_path(self, p: int) -> None:
        """根から葉pまでの経路上の作用を下へ流す。O(log N)"""
        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)

    def _all_apply(self, k: int, f: typing.Any) -> None:
        """ノードkに作用fを積む（葉なら値に直接適用する）。O(1)"""
        if k < self._size:
            self._lz[k] = self._composition(f, self._lz[k])
        else:
            p = k - self._size
            if p < self._n:
                self._d[p] = self._mapping(f, self._d[p])

    def _push(self, k: int) -> None:
        """ノードkの作用を子に流す。O(1)"""
        if self._lz[k] == self._id:
            return
        self._all_apply(2 * k, self._lz[k])
        self._all_apply(2 * k + 1, self._lz[k])
        self._lz[k] = self._id
