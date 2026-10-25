from typing import Sequence, TypeVar

T = TypeVar("T")


def prefix_function(s: Sequence[T]) -> list[int]:
    """KMP 法の失敗関数。pi[i] は s[:i + 1] の、真の接頭辞かつ接尾辞である最長の長さ。O(N)

    最小周期（s が長さ p の文字列の繰り返しで書けるような最小の p）は len(s) - pi[-1]。
    ac-library-python の z_algorithm でも検索はできるが、周期や境界（border）を扱うときはこちらが便利。

    使い方:
        prefix_function("abacaba")         # [0, 0, 1, 0, 1, 2, 3]
        s = "abcabcab"
        len(s) - prefix_function(s)[-1]    # 3（最小周期）

    https://github.com/yasyasyu/local-lib/blob/master/kmp.py
    """
    n = len(s)
    pi = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_search(text: Sequence[T], pattern: Sequence[T]) -> list[int]:
    """text の中で pattern が現れる開始位置を、重なりも含めてすべて返す（KMP 法）。O(|text| + |pattern|)

    pattern が空なら、0 から len(text) までのすべての位置を返す。

    使い方:
        kmp_search("abababa", "aba")   # [0, 2, 4]
        kmp_search("abc", "d")         # []

    https://github.com/yasyasyu/local-lib/blob/master/kmp.py
    """
    m = len(pattern)
    if m == 0:
        return list(range(len(text) + 1))
    pi = prefix_function(pattern)
    res = []
    k = 0  # 今一致している pattern の長さ
    for i, c in enumerate(text):
        while k > 0 and c != pattern[k]:
            k = pi[k - 1]
        if c == pattern[k]:
            k += 1
        if k == m:
            res.append(i - m + 1)
            k = pi[k - 1]
    return res
