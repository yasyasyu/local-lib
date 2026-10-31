import math


class SmallestPrimeFactor:
    """最小素因数の篩。N 以下の整数の素因数分解を、1個あたり O(log x) で行う

    構築は O(N log log N)。たくさんの数（N は 10**7 程度まで）を素因数分解するときに使う。
    1個だけ・大きい数（10**18 程度）を分解するなら pollard_rho.py を使う。

    使い方::

        spf = SmallestPrimeFactor(10**6)
        spf.factorize(360)      # {2: 3, 3: 2, 5: 1}
        spf.is_prime(97)        # True
        spf.divisors(12)        # [1, 2, 3, 4, 6, 12]
        spf.spf[12]             # 2（12 の最小素因数）

    https://github.com/yasyasyu/local-lib/blob/master/smallest_prime_factor.py
    """

    def __init__(self, N: int) -> None:
        """N 以下の整数の最小素因数を求める。O(N log log N)"""
        self.N = N
        # spf[x]: x の最小素因数（spf[0] = 0, spf[1] = 1 とする）
        spf = list(range(N + 1))
        is_prime = bytearray([1]) * (N + 1)
        primes = []
        for p in range(2, math.isqrt(N) + 1):
            if is_prime[p]:
                is_prime[p * p :: p] = bytes(len(range(p * p, N + 1, p)))
                primes.append(p)
        # 大きい素数から順に倍数へ書き込むと、最後に書くのが最小の素因数になる
        for p in reversed(primes):
            spf[p * p :: p] = [p] * len(range(p * p, N + 1, p))
        self.spf = spf

    def is_prime(self, x: int) -> bool:
        """x（N 以下）が素数かを返す。O(1)"""
        return x >= 2 and self.spf[x] == x

    def factorize(self, x: int) -> dict[int, int]:
        """x（1 以上 N 以下）を素因数分解し、{素数: 指数} を素数の昇順で返す。O(log x)"""
        res: dict[int, int] = {}
        spf = self.spf
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            res[p] = e
        return res

    def divisors(self, x: int) -> list[int]:
        """x（1 以上 N 以下）の約数を昇順で返す。O(d(x) log d(x))（d(x) は約数の個数）"""
        divs = [1]
        for p, e in self.factorize(x).items():
            divs = [d * p**k for d in divs for k in range(e + 1)]
        divs.sort()
        return divs
