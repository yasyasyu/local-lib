class Mo:
    """Moのアルゴリズム（オフラインで区間クエリをならしO((N+Q)sqrt(N))で処理する）

    add/removeで「集合に要素iを足す/抜く」差分更新だけを実装すれば、
    クエリを良い順番で処理することで全体を高速化できる。

    使い方:
        mo = Mo(N)
        for l, r in queries:  # 半開区間[l, r)
            mo.add_query(l, r)

        count = [0] * MAX_VALUE
        distinct = 0

        def add(i):
            nonlocal distinct
            if count[a[i]] == 0:
                distinct += 1
            count[a[i]] += 1

        def remove(i):
            nonlocal distinct
            count[a[i]] -= 1
            if count[a[i]] == 0:
                distinct -= 1

        def answer():
            return distinct

        answers = mo.solve(add, remove, answer)
        # answers[k] は k番目にadd_queryした区間（= queries[k]）に対する答え

    https://github.com/yasyasyu/local-lib/blob/master/mo.py
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.queries: list[tuple[int, int]] = []

    def add_query(self, l: int, r: int) -> int:
        """半開区間[l, r)へのクエリを追加する。追加した順番（0-indexed）を返す。"""
        self.queries.append((l, r))
        return len(self.queries) - 1

    def solve(self, add, remove, answer) -> list:
        """全クエリを処理し、add_queryした順番に対応する答えのリストを返す。"""
        q = len(self.queries)
        if q == 0:
            return []

        block = max(1, int(self.n / max(1, q**0.5)))

        def sort_key(i):
            l, r = self.queries[i]
            block_id = l // block
            return (block_id, r if block_id % 2 == 0 else -r)

        order = sorted(range(q), key=sort_key)

        res = [None] * q
        cur_l, cur_r = 0, 0
        for idx in order:
            l, r = self.queries[idx]
            while cur_l > l:
                cur_l -= 1
                add(cur_l)
            while cur_r < r:
                add(cur_r)
                cur_r += 1
            while cur_l < l:
                remove(cur_l)
                cur_l += 1
            while cur_r > r:
                cur_r -= 1
                remove(cur_r)
            res[idx] = answer()

        return res
