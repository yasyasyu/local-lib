from typing import Callable, Generic, Sequence, TypeVar

T = TypeVar("T")


class SparseTable(Generic[T]):
    """Sparse Table。変更のない配列の区間集約を、構築 O(N log N)・クエリ O(1) で求める

    op は冪等（op(x, x) = x）で結合的な演算に限る（min・max・gcd・and・or など。足し算は不可）。
    区間を重なりのある2つの区間で覆って求めるため。値の更新はできない（必要なら SegTree）。
    クエリのメソッド名は ac-library-python の SegTree に合わせて prod にしている。

    使い方:
        st = SparseTable([3, 1, 4, 1, 5, 9, 2, 6])         # 既定は min
        st.prod(2, 5)                                     # 1（a[2:5] = [4, 1, 5] の最小値）
        SparseTable([3, 1, 4, 1, 5], op=max).prod(0, 3)   # 4

        from math import gcd
        SparseTable([12, 18, 8], op=gcd).prod(0, 2)       # 6

    https://github.com/yasyasyu/local-lib/blob/master/sparse_table.py
    """

    def __init__(self, v: Sequence[T], op: Callable[[T, T], T] = min) -> None:
        """配列 v から構築する。O(N log N)"""
        self.op = op
        self.n = len(v)
        # table[k][i] = op(v[i], ..., v[i + 2**k - 1])
        self.table = [list(v)]
        k = 1
        while (1 << k) <= self.n:
            prev = self.table[-1]
            half = 1 << (k - 1)
            self.table.append(
                [op(prev[i], prev[i + half]) for i in range(self.n - (1 << k) + 1)]
            )
            k += 1

    def prod(self, l: int, r: int) -> T:
        """op(v[l], ..., v[r - 1]) を返す。l < r であること（空の区間は不可）。O(1)"""
        k = (r - l).bit_length() - 1
        row = self.table[k]
        return self.op(row[l], row[r - (1 << k)])
