def mat_mul(
    A: list[list[int]], B: list[list[int]], mod: int | None = None
) -> list[list[int]]:
    """行列の積 A * B を計算する。

    https://github.com/yasyasyu/local-lib/blob/master/matrix_pow.py
    """
    n, m, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        Ai, Ci = A[i], C[i]
        for k in range(m):
            aik = Ai[k]
            if aik == 0:
                continue
            Bk = B[k]
            for j in range(p):
                Ci[j] += aik * Bk[j]
        if mod:
            for j in range(p):
                Ci[j] %= mod
    return C


def mat_pow(A: list[list[int]], k: int, mod: int | None = None) -> list[list[int]]:
    """正方行列Aのk乗を繰り返し二乗法で計算する。

    使い方:
        A = [[1, 1], [1, 0]]  # フィボナッチ数列の遷移行列
        A_k = mat_pow(A, 10, mod=10**9 + 7)
        A_k[0][1]             # フィボナッチ数列 F(10)

    https://github.com/yasyasyu/local-lib/blob/master/matrix_pow.py
    """
    n = len(A)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in A]
    while k:
        if k & 1:
            result = mat_mul(result, base, mod)
        base = mat_mul(base, base, mod)
        k >>= 1
    return result
