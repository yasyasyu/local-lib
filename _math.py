import math


def divisors(n) -> list[int]:
    """nの約数を昇順に列挙する。
    divisors(12)                  # [1, 2, 3, 4, 6, 12]

    https://github.com/yasyasyu/local-lib/blob/master/_math.py
    """
    lower, upper = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            lower.append(i)
            if i != n // i:
                upper.append(n // i)
        i += 1
    return lower + upper[::-1]


def Eratosthenes(N) -> list[int]:
    """N以下の素数を列挙する（エラトステネスの篩）。
    Eratosthenes(30)               # [2, 3, 5, 7, ..., 29]（30以下の素数）

    https://github.com/yasyasyu/local-lib/blob/master/_math.py
    """
    prime = [2]
    data = [i + 1 for i in range(2, N, 2)]
    while data:
        p = data[0]
        prime.append(p)
        data = [e for e in data if (e % p != 0)]
        if int(N**0.5) <= p:
            return prime + data
    return prime


def prime_factorize(N) -> dict[int, int]:
    """Nを素因数分解し、{素数: 指数} の defaultdict を返す。
    prime_factorize(360)     # {2: 3, 3: 2, 5: 1}

    https://github.com/yasyasyu/local-lib/blob/master/_math.py
    """
    from collections import defaultdict

    prime = defaultdict(int)
    while N % 2 == 0:
        prime[2] += 1
        N //= 2
    factor = 3
    while factor * factor <= N:
        if N % factor == 0:
            prime[factor] += 1
            N //= factor
        else:
            factor += 2
    if N != 1:
        prime[N] += 1

    return prime


def section_prime_sieve(L, R) -> list[bool]:
    """区間 [L, R] の各整数が素数かどうかを判定する（区間篩）。
    section_prime_sieve(14, 30)    # [L,R]の各値が素数かどうかのbool列

    戻り値は長さ R-L+1 のbool列で、値vの判定結果は is_prime_section[v-L] に入る。

    https://github.com/yasyasyu/local-lib/blob/master/_math.py
    """
    # √R 以下の素数を炙り出すための篩
    sqrt_R = int(math.sqrt(R) + 0.1)
    is_prime = [True] * (sqrt_R + 1)

    # L 以上 R 以下の整数vが素数かどうか
    # その答えは is_prime_section[v-L] に格納される
    is_prime_section = [True] * (R - L + 1)

    # 篩
    for p in range(2, sqrt_R + 1):
        # すでに合成数であるものはスキップする
        if not is_prime[p]:
            continue

        # p 以外の p の倍数から素数ラベルを剥奪
        q = p * 2
        while q * q <= R:
            is_prime[q] = False
            q += p

        # L 以上の最小の p の倍数
        start = -(-L // p) * p
        if start == p:
            start = p * 2

        # L 以上 R 以下の整数のうち、p の倍数をふるう
        q = start
        while q <= R:
            is_prime_section[q - L] = False
            q += p

    # 1 は素数ではないが、上記のふるいでは素数の倍数としては除外されない
    if L <= 1 <= R:
        is_prime_section[1 - L] = False

    return is_prime_section
