import typing


class MonoidUnionFind:
    """集合ごとにモノイドの値を載せたUnion-Find（セグ木のop / vのように値の載せ方を一般化したもの）

    集合ごとに値を1つ持ち、mergeで2つの集合の値をopでまとめる。
    要素数・和・最小値・最大値・辺の本数などを、クラスを改造せずに管理できる。

    op: 2つの集合の値をまとめる関数。結合的かつ可換であること
        （union by sizeでどちらが根になるかが決まるので、まとめる順番は制御できない）
    v:  各要素の初期値のリスト

    計算量: find / merge / same / get / applyはならしO(α(N))（opとfの呼び出しをO(1)とした場合）

    使い方:
        # 集合ごとの和
        uf = MonoidUnionFind(lambda a, b: a + b, [3, 1, 4, 1, 5])
        uf.merge(0, 1)
        uf.get(1)          # 4
        uf.size(0)         # 2（要素数はvに関係なく常に取れる）

        # 同じ集合内に張った辺の本数を数える（閉路判定など）: 値を(頂点数, 辺数)で持つ
        uf = MonoidUnionFind(lambda a, b: (a[0] + b[0], a[1] + b[1]), [(1, 0)] * 4)
        for u, v in [(0, 1), (1, 2), (2, 0)]:
            uf.merge(u, v)                           # 同じ集合なら何もしない（Falseが返る）
            uf.apply(u, lambda d: (d[0], d[1] + 1))  # どちらの場合も、張った辺を1本数える
        uf.get(0)          # (3, 3) -> 辺数 >= 頂点数なので閉路がある

    要素リストのマージテク・mergeの取り消しなど、値の載せ方で表せない改造は
    union_find.pyをコピーして改造すること。

    https://github.com/yasyasyu/local-lib/blob/master/monoid_union_find.py
    """

    def __init__(
        self,
        op: typing.Callable[[typing.Any, typing.Any], typing.Any],
        v: typing.List[typing.Any],
    ) -> None:
        """各要素の初期値vで初期化する。O(N)"""
        self._op = op
        self._n = len(v)
        # parent[x] < 0 のときxは根で、-parent[x]がその集合の要素数
        self._parent = [-1] * self._n
        # data[r]: 根rの集合の値（根以外の要素の値は古いので読まない）
        self._data = list(v)

    def find(self, x: int) -> int:
        """xの属する集合の代表元を返す。ならしO(α(N))"""
        root = x
        while self._parent[root] >= 0:
            root = self._parent[root]
        while self._parent[x] >= 0:
            self._parent[x], x = root, self._parent[x]
        return root

    def merge(self, x: int, y: int) -> bool:
        """xとyの属する集合を併合し、値をopでまとめる。既に同じ集合ならFalseを返す。ならしO(α(N))"""
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        if self._parent[x] > self._parent[y]:
            x, y = y, x
        # 要素数の大きい方の根xに、yを付ける
        self._parent[x] += self._parent[y]
        self._parent[y] = x
        self._data[x] = self._op(self._data[x], self._data[y])
        return True

    def same(self, x: int, y: int) -> bool:
        """xとyが同じ集合に属するかを返す。ならしO(α(N))"""
        return self.find(x) == self.find(y)

    def get(self, x: int) -> typing.Any:
        """xの属する集合の値を返す。ならしO(α(N))"""
        return self._data[self.find(x)]

    def apply(self, x: int, f: typing.Callable[[typing.Any], typing.Any]) -> None:
        """xの属する集合の値をf(値)に置き換える。ならしO(α(N))"""
        r = self.find(x)
        self._data[r] = f(self._data[r])

    def size(self, x: int) -> int:
        """xの属する集合の要素数を返す。ならしO(α(N))"""
        return -self._parent[self.find(x)]

    def groups(self) -> typing.List[typing.List[int]]:
        """集合ごとの要素のリストを返す。O(N α(N))"""
        G = [[] for _ in range(self._n)]
        for i in range(self._n):
            G[self.find(i)].append(i)
        return [g for g in G if g]
