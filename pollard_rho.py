from math import gcd

_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
# n < 2**64 なら、この7つの底で Miller-Rabin 判定が確定的に正しくなる
_MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def is_prime(n: int) -> bool:
    """n が素数かを判定する（Miller-Rabin 法）。O(log n) 回の pow(・, ・, n)

    n < 2**64（約 1.8 * 10**18）の範囲では、確定的に正しい答えを返す。
    それより大きい n でも動くが、まれに合成数を素数と判定する可能性がある。

    使い方::

        is_prime(998244353)            # True
        is_prime(10**18 + 9)           # True
        is_prime(561)                  # False（カーマイケル数）

    https://github.com/yasyasyu/local-lib/blob/master/pollard_rho.py
    """
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _find_factor(n: int) -> int:
    """合成数 n（奇数）の、1 と n 以外の約数を1つ返す（Pollard の ρ 法、Brent の改良版）"""
    m = 128  # gcd をまとめて取る間隔
    c = 1
    while True:
        y, r, q, g = 2, 1, 1, 1
        x = ys = 2
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            # まとめた中で n の倍数になった。1歩ずつやり直して約数を探す
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g
        c += 1  # 失敗したので、乱数列 x -> x^2 + c の c を変えてやり直す


def factorize(n: int) -> dict[int, int]:
    """n（1 以上）を素因数分解し、{素数: 指数} を素数の昇順で返す（Pollard の ρ 法）。期待 O(n^(1/4)) 程度

    10**18 程度の数でも高速に分解できる（_math.prime_factorize は試し割りなので 10**12 程度まで）。
    たくさんの小さい数を分解するなら smallest_prime_factor.py の方が速い。

    使い方::

        factorize(360)                         # {2: 3, 3: 2, 5: 1}
        factorize(999999999999999989 * 2)      # {2: 1, 999999999999999989: 1}
        factorize(1)                           # {}

    https://github.com/yasyasyu/local-lib/blob/master/pollard_rho.py
    """
    res: dict[int, int] = {}
    # 小さい素因数は試し割りで先に取り除く
    for p in _SMALL_PRIMES:
        while n % p == 0:
            res[p] = res.get(p, 0) + 1
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if is_prime(m):
            res[m] = res.get(m, 0) + 1
            continue
        d = _find_factor(m)
        stack.append(d)
        stack.append(m // d)
    return dict(sorted(res.items()))
