from typing import Callable, Sequence, TypeVar

T = TypeVar("T")
K = TypeVar("K")

# 分数 a/b を (a, b) で表す
Frac = tuple[int, int]

# 比較関数はすべて cmp_sort.sort_by_cmp と同じ約束:
#     cmp(x, y) が負なら x が前、正なら y が前、0 ならどちらでもよい。
# キー関数で書ける並べ方なら、sorted(key=...) の方が速い。ここの比較関数は、
# キーで書けない（キーにすると誤差が出る）ときや、複数の基準を組み合わせるときに使う。


def frac_cmp(p: Frac, q: Frac) -> int:
    """分数 p = a/b と q = c/d を、浮動小数点を使わずに比べる（小さい方が前）。O(1)

    分母が負でもよい。分母が0のときは、分子の符号に応じて +∞ / -∞ として扱う。
    0/0 は渡さないこと（どの値とも等しくなり、順序が壊れる）。
    a/b を浮動小数点で計算して比べると、値の近い分数を区別できないことがある。

    使い方::

        frac_cmp((1, 3), (1, 2))  # 負（1/3 < 1/2）
        frac_cmp((1, 2), (2, 4))  # 0（等しい）

        # 成功率 A[i] / (A[i] + B[i]) の高い順、同率は番号の小さい順（ABC308 C）
        order = sort_by_cmp(range(N), reverse_cmp(key_cmp(lambda i: (A[i], A[i] + B[i]), frac_cmp)))

    https://github.com/yasyasyu/local-lib/blob/master/comparators.py
    """
    a, b = p
    c, d = q
    if b < 0:
        a, b = -a, -b
    if d < 0:
        c, d = -c, -d
    if b == 0 and d == 0:
        # 両方 ±∞ のときは、外積だけでは +∞ と -∞ を区別できない
        return ((a > 0) - (a < 0)) - ((c > 0) - (c < 0))
    return a * d - c * b


def concat_cmp(x: str, y: str) -> int:
    """x + y が y + x より小さいとき x を前にする比較。O(len(x) + len(y))

    この順に並べてつなげると、つなげた文字列が辞書順最小になる（推移律が成り立つことが知られている）。
    最大にしたいときは reverse_cmp(concat_cmp) を使う。

    使い方::

        "".join(sort_by_cmp(["3", "30", "34"], concat_cmp))               # "30334"（最小）
        "".join(sort_by_cmp(["3", "30", "34"], reverse_cmp(concat_cmp)))  # "34330"（最大）

    https://github.com/yasyasyu/local-lib/blob/master/comparators.py
    """
    xy = x + y
    yx = y + x
    return (xy > yx) - (xy < yx)


def exchange_cmp(cost: Callable[[T, T], int]) -> Callable[[T, T], int]:
    """交換論法の比較関数を作る。cost(a, b) < cost(b, a) なら a を前にする。O(1)（cost 2回）

    :param cost: cost(a, b)。隣り合う a, b を「a, b の順」に置いたときのコスト
        （並べ順で変わる部分だけでよい。前後にある他の要素の影響は受けないこと）。

    注意: 「隣を入れ替えて得なら入れ替える」で決まる順序は、推移律が成り立つとは限らない。
    成り立たないとソートの結果がおかしくなるので、check_cmp で小さいデータを確かめておくとよい。
    多くの場合は、ある値の比（frac_cmp）の比較に帰着する。

    使い方::

        # 処理時間 p・重み w のタスクを順に処理し、(重み × 完了時刻) の総和を最小にする
        tasks = [(3, 1), (1, 2), (2, 2)]  # (p, w)
        cost = lambda a, b: a[1] * a[0] + b[1] * (a[0] + b[0])
        sort_by_cmp(tasks, exchange_cmp(cost))  # [(1, 2), (2, 2), (3, 1)]

    https://github.com/yasyasyu/local-lib/blob/master/comparators.py
    """

    def cmp(a: T, b: T) -> int:
        return cost(a, b) - cost(b, a)

    return cmp


def key_cmp(
    key: Callable[[T], K], cmp: Callable[[K, K], int] | None = None
) -> Callable[[T, T], int]:
    """key で変換した値どうしを比べる比較関数を作る。cmp を省略すると < で比べる。O(1)（key 2回）

    then_cmp で他の比較関数とつなげるとき、要素をそのまま比較関数に渡せないとき
    （添字を並べ替えたいときなど）に使う。key だけで済むなら sorted(key=key) の方が速い。

    使い方::

        # 添字を、点 P[i] の偏角の順に並べる
        sort_by_cmp(range(N), key_cmp(lambda i: P[i], arg_cmp))

    https://github.com/yasyasyu/local-lib/blob/master/comparators.py
    """
    if cmp is None:

        def natural(x: T, y: T) -> int:
            kx = key(x)
            ky = key(y)
            return (kx > ky) - (kx < ky)

        return natural

    def mapped(x: T, y: T) -> int:
        return cmp(key(x), key(y))

    return mapped


def reverse_cmp(cmp: Callable[[T, T], int]) -> Callable[[T, T], int]:
    """cmp の逆順（降順）にする比較関数を作る。O(1)

    使い方::

        sort_by_cmp(fracs, reverse_cmp(frac_cmp))  # 分数の大きい順

    https://github.com/yasyasyu/local-lib/blob/master/comparators.py
    """

    def rev(x: T, y: T) -> int:
        return cmp(y, x)

    return rev


def then_cmp(*cmps: Callable[[T, T], int]) -> Callable[[T, T], int]:
    """比較関数を優先順につなげる。前の比較関数で等しい（0）ときだけ、次の比較関数で比べる。O(len(cmps))

    使い方::

        # 偏角の昇順、同じ偏角なら原点に近い順
        cmp = then_cmp(arg_cmp, key_cmp(lambda p: p[0] * p[0] + p[1] * p[1]))
        sort_by_cmp(points, cmp)

        # 1つ目の値の昇順、同じなら2つ目の値の降順
        cmp = then_cmp(key_cmp(lambda t: t[0]), reverse_cmp(key_cmp(lambda t: t[1])))

    https://github.com/yasyasyu/local-lib/blob/master/comparators.py
    """

    def chained(x: T, y: T) -> int:
        for c in cmps:
            r = c(x, y)
            if r:
                return r
        return 0

    return chained


def check_cmp(items: Sequence[T], cmp: Callable[[T, T], int]) -> tuple[T, ...] | None:
    """cmp が items の上で正しい順序（全前順序）になっているかを全組で調べる（デバッグ用）。O(N^3)

    :return: 正しければ None。崩れていれば、その原因になった要素の組（中身は下）。
    :rtype: tuple[T, ...] | None

    - (x,): cmp(x, x) が0でない
    - (x, y): cmp(x, y) と cmp(y, x) の符号が逆になっていない
    - (x, y, z): x <= y かつ y <= z なのに x <= z でない（推移律が成り立たない）

    交換論法などで作った比較関数を、小さいデータ（N は数十まで）で確かめるのに使う。

    使い方::

        check_cmp(small_tasks, exchange_cmp(cost))  # None なら、この範囲ではソートに使ってよい

    https://github.com/yasyasyu/local-lib/blob/master/comparators.py
    """
    n = len(items)
    le = [[False] * n for _ in range(n)]  # le[i][j]: items[i] <= items[j]
    for i in range(n):
        x = items[i]
        if cmp(x, x) != 0:
            return (x,)
        for j in range(n):
            y = items[j]
            r = cmp(x, y)
            s = cmp(y, x)
            if (r > 0) - (r < 0) != (s < 0) - (s > 0):
                return (x, y)
            le[i][j] = r <= 0
    for j in range(n):
        for i in range(n):
            if not le[i][j]:
                continue
            for k in range(n):
                if le[j][k] and not le[i][k]:
                    return (items[i], items[j], items[k])
    return None
