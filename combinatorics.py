class Combinatorics:
    """mod付き組合せ論（階乗・逆元テーブルによるnCr等の高速計算）

    modは素数である必要がある（フェルマーの小定理で逆元を求めるため）。

    使い方:
        MOD = 998244353
        comb = Combinatorics(10**6, MOD)
        comb.fact(5)      # 5! mod MOD = 120
        comb.perm(5, 2)   # 5P2 mod MOD = 20
        comb.cmb(5, 2)    # 5C2 mod MOD = 10
        comb.hcm(5, 2)    # 重複組合せ 5H2 mod MOD = 15

    https://github.com/yasyasyu/local-lib/blob/master/combinatorics.py
    """

    def __init__(self, max_n: int, mod: int) -> None:
        self.mod = mod
        self.max_n = max_n
        self.factorial = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            self.factorial[i] = self.factorial[i - 1] * i % mod
        self.inv_factorial = [1] * (max_n + 1)
        self.inv_factorial[max_n] = pow(self.factorial[max_n], mod - 2, mod)
        for i in range(max_n, 0, -1):
            self.inv_factorial[i - 1] = self.inv_factorial[i] * i % mod

    def fact(self, n: int) -> int:
        """n! mod pを返す。"""
        return self.factorial[n]

    def inv_fact(self, n: int) -> int:
        """(n!)^-1 mod pを返す。"""
        return self.inv_factorial[n]

    def perm(self, n: int, r: int) -> int:
        """nPr mod pを返す。0<=r<=nでない場合は0。"""
        if r < 0 or r > n:
            return 0
        return self.factorial[n] * self.inv_factorial[n - r] % self.mod

    def cmb(self, n: int, r: int) -> int:
        """nCr mod pを返す。0<=r<=nでない場合は0。"""
        if r < 0 or r > n:
            return 0
        return (
            self.factorial[n]
            * self.inv_factorial[r]
            % self.mod
            * self.inv_factorial[n - r]
            % self.mod
        )

    def hcm(self, n: int, r: int) -> int:
        """重複組合せ nHr (= (n+r-1)Cr) mod pを返す。"""
        if n == 0:
            return 1 if r == 0 else 0
        return self.cmb(n + r - 1, r)
