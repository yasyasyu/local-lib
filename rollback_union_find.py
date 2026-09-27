class RollbackUnionFind:
    """rollback（undo）可能なUnion-Find

    経路圧縮を行わない代わりに、直前までのmergeを元に戻せる。
    union by sizeによりfindはO(log N)。

    使い方:
        uf = RollbackUnionFind(5)
        uf.merge(0, 1)
        state = uf.snapshot()
        uf.merge(1, 2)
        uf.same(0, 2)     # True
        uf.rollback(state)
        uf.same(0, 2)     # False

        uf.merge(2, 3)
        uf.undo()         # 直前のmergeを1回分だけ元に戻す
        uf.same(2, 3)     # False

    https://github.com/yasyasyu/local-lib/blob/master/rollback_union_find.py
    """

    def __init__(self, N: int) -> None:
        """要素数Nで初期化する。O(N)"""
        self.parent = [-1] * N
        self.history: list[tuple[int, int, int, int] | None] = []

    def find(self, x: int) -> int:
        """xの属する集合の代表元を返す。O(log N)"""
        while self.parent[x] >= 0:
            x = self.parent[x]
        return x

    def size(self, x: int) -> int:
        """xの属する集合の要素数を返す。O(log N)"""
        return -self.parent[self.find(x)]

    def same(self, x: int, y: int) -> bool:
        """xとyが同じ集合に属するかを返す。O(log N)"""
        return self.find(x) == self.find(y)

    def merge(self, x: int, y: int) -> bool:
        """xとyを併合する。すでに同じ集合だった場合はFalseを返す。O(log N)"""
        x, y = self.find(x), self.find(y)
        if x == y:
            self.history.append(None)
            return False
        if self.parent[x] > self.parent[y]:
            x, y = y, x
        self.history.append((x, self.parent[x], y, self.parent[y]))
        self.parent[x] += self.parent[y]
        self.parent[y] = x
        return True

    def snapshot(self) -> int:
        """現在の状態を表すスナップショットを返す（rollback()に渡す）。O(1)"""
        return len(self.history)

    def undo(self) -> None:
        """直前のmerge操作を1回分元に戻す。O(1)"""
        record = self.history.pop()
        if record is None:
            return
        x, px, y, py = record
        self.parent[x] = px
        self.parent[y] = py

    def rollback(self, state: int) -> None:
        """snapshot()で取得した状態まで巻き戻す。O(戻すmergeの回数)"""
        while len(self.history) > state:
            self.undo()
