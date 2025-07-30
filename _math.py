import math


def divisors(n):
    lower, upper = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            lower.append(i)
            if i != n // i:
                upper.append(n // i)
        i += 1
    return lower + upper[::-1]


def Eratosthenes(N):
    prime = [2]
    data = [i + 1 for i in range(2, N, 2)]
    while True:
        p = data[0]
        if int(N**0.5) <= p:
            return prime + data
        prime.append(p)
        data = [e for e in data if (e % p != 0)]


def prime_factorize(N):
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


def section_prime_sieve(L, R):
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
        start = --L // p * p
        if start == p:
            start = p * 2

        # L 以上 R 以下の整数のうち、p の倍数をふるう
        q = start
        while q <= R:
            is_prime_section[q - L] = False
            q += p

    return is_prime_section
