def divisors(n):
    lower_divisors, upper_divisors = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n // i)
        i += 1
    return lower_divisors + upper_divisors[::-1]


def Eratosthenes(N):
    prime = [2]
    Lim = int(N**0.5)
    data = [i + 1 for i in range(2, N, 2)]
    while True:
        p = data[0]
        if Lim <= p:
            return prime + data
        prime.append(p)
        data = [e for e in data if (e % p != 0)]


def prime_factorize(n):
    a = []
    while n % 2 == 0:
        a.append(2)
        n //= 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            a.append(f)
            n //= f
        else:
            f += 2
    if n != 1:
        a.append(n)
    return a
