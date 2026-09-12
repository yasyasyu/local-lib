import bisect


class LiChaoTree:
    """Li Chao Tree（直線の追加とある点での最小値クエリをO(log N)で処理する）

    最小値クエリ用。最大値がほしい場合は追加するa, bの符号を反転し、
    query()の結果も反転すればよい。

    使い方:
        xs = [0, 1, 2, 3, 4, 5]  # クエリしうるxの候補をあらかじめ列挙しておく
        lct = LiChaoTree(xs)
        lct.add_line(1, 0)     # y = 1*x + 0 を追加
        lct.add_line(-1, 10)   # y = -1*x + 10 を追加
        lct.query(3)           # x=3における最小値 -> min(1*3+0, -1*3+10) = 3

    https://github.com/yasyasyu/local-lib/blob/master/li_chao_tree.py
    """

    INF = float("inf")

    def __init__(self, xs: list[int]) -> None:
        xs = sorted(set(xs))
        n = max(len(xs), 1)
        self.size = 1
        while self.size < n:
            self.size *= 2
        pad = xs[-1] if xs else 0
        self.xs = xs + [pad] * (self.size - len(xs))
        self.line = [(0, self.INF)] * (2 * self.size)

    def _f(self, line: tuple[int, float], x: int) -> float:
        a, b = line
        return a * x + b

    def add_line(self, a: int, b: int) -> None:
        """直線 y = a*x + b を追加する。"""
        line = (a, b)
        node, l, r = 1, 0, self.size
        while True:
            m = (l + r) // 2
            left_better = self._f(line, self.xs[l]) < self._f(
                self.line[node], self.xs[l]
            )
            mid_better = self._f(line, self.xs[m]) < self._f(
                self.line[node], self.xs[m]
            )
            if mid_better:
                self.line[node], line = line, self.line[node]
                left_better = not left_better
            if r - l == 1:
                return
            if left_better:
                node, r = node * 2, m
            else:
                node, l = node * 2 + 1, m

    def query(self, x: int) -> float:
        """xにおける直線群の最小値を返す。"""
        idx = bisect.bisect_left(self.xs, x, 0, self.size)
        node, l, r = 1, 0, self.size
        res = self._f(self.line[node], x)
        while r - l > 1:
            m = (l + r) // 2
            if idx < m:
                node, r = node * 2, m
            else:
                node, l = node * 2 + 1, m
            res = min(res, self._f(self.line[node], x))
        return res
