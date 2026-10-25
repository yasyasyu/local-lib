from typing import Sequence, TypeVar

T = TypeVar("T")


def manacher(s: Sequence[T]) -> list[int]:
    """各 i について、s[i] を中心とする奇数長の最長回文の半径を返す（Manacher 法）。O(N)

    戻り値 r: s[i - r[i] + 1 : i + r[i]] が回文で、その長さは 2 * r[i] - 1。
    偶数長の回文も扱うなら palindrome_lengths を使う。

    使い方:
        manacher("abaaba")   # [1, 2, 1, 1, 2, 1]（"aba" の中心は半径2）

    https://github.com/yasyasyu/local-lib/blob/master/manacher.py
    """
    n = len(s)
    r = [0] * n
    i = j = 0  # i: 中心、j: その半径
    while i < n:
        while i - j >= 0 and i + j < n and s[i - j] == s[i + j]:
            j += 1
        r[i] = j
        # 回文の内側では、中心に対して対称な位置の半径をそのまま使える
        k = 1
        while i - k >= 0 and k + r[i - k] < j:
            r[i + k] = r[i - k]
            k += 1
        i += k
        j -= k
    return r


def palindrome_lengths(s: Sequence[T]) -> list[int]:
    """各中心について、最長の回文の長さを返す（偶数長も含む）。O(N)

    戻り値 L は長さ 2N - 1:
        L[2 * i]     = s[i] を中心とする最長回文の長さ（奇数）
        L[2 * i + 1] = s[i] と s[i + 1] の間を中心とする最長回文の長さ（偶数、0 もありうる）
    s[l:r] が回文 ⇔ L[l + r - 1] >= r - l（l < r）。

    使い方:
        L = palindrome_lengths("abba")   # [1, 0, 1, 4, 1, 0, 1]
        max(L)                           # 4（最長の回文の長さ）
        L[0 + 4 - 1] >= 4                # True（"abba" は回文）

    https://github.com/yasyasyu/local-lib/blob/master/manacher.py
    """
    n = len(s)
    if n == 0:
        return []
    # 文字の間に番兵 None を挟むと、偶数長の回文も奇数長として扱える
    t: list[T | None] = [None] * (2 * n - 1)
    t[::2] = s
    r = manacher(t)
    # t の回文 t[k - r + 1 : k + r] に含まれる元の文字の個数が、元の回文の長さ
    res = []
    for k in range(2 * n - 1):
        if k % 2 == 0:
            # 文字が中心: r が奇数なら両端が文字で r 個、偶数なら両端が番兵で r - 1 個
            res.append(2 * ((r[k] + 1) // 2) - 1)
        else:
            # 番兵が中心: r が偶数なら両端が文字で r 個、奇数なら両端が番兵で r - 1 個
            res.append(2 * (r[k] // 2))
    return res
