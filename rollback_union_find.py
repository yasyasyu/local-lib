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
        self.parent = [-1] * N
        self.history: list[tuple[int, int, int, int] | None] = []

    def find(self, x: int) -> int:
        while self.parent[x] >= 0:
            x = self.parent[x]
        return x

    def size(self, x: int) -> int:
        return -self.parent[self.find(x)]

    def same(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def merge(self, x: int, y: int) -> bool:
        """xとyを併合する。すでに同じ集合だった場合はFalseを返す。"""
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
        """現在の状態を表すスナップショットを返す（rollback()に渡す）。"""
        return len(self.history)

    def undo(self) -> None:
        """直前のmerge操作を1回分元に戻す。"""
        record = self.history.pop()
        if record is None:
            return
        x, px, y, py = record
        self.parent[x] = px
        self.parent[y] = py

    def rollback(self, state: int) -> None:
        """snapshot()で取得した状態まで巻き戻す。"""
        while len(self.history) > state:
            self.undo()
