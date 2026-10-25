from typing import Callable, Iterable

from .cmp_sort import sort_by_cmp

# 整数座標の点 (x, y)。誤差なく比較するため整数に限る
IntPoint = tuple[int, int]

# 偏角ソートの方針
#   - atan2 は使わない。浮動小数点の誤差で、偏角の近い点を区別できなくなる
#     （例: (10**9, 10**9 - 1) と (10**9 - 1, 10**9 - 2) で atan2 の値が一致する）。
#   - 外積だけでは一周ぶんの順序にならない（推移律が壊れる）。
#     そこで、始線から半周ぶんずつの2つの半平面に分け、同じ半平面の中だけ外積で比べる。
#   - 原点は外積が誰とでも0になり、どの点とも「等しい」ことになって推移律が壊れる。
#     原点は専用のグループにして、先頭に置く。


def _arg_group(p: IntPoint, dx: int, dy: int, closed: bool) -> int:
    """点 p が属するグループを返す。0: 原点、1: 始線から半周、2: 残りの半周。O(1)"""
    c = dx * p[1] - dy * p[0]  # 始線 × p
    if c > 0:
        return 1
    if c < 0:
        return 2
    # 始線と同じ向き・逆向き・原点のどれか
    d = dx * p[0] + dy * p[1]
    if d == 0:
        return 0
    # closed: 始線と同じ向きの点を先頭に置く。open: 末尾に置く
    return 1 if (d > 0) == closed else 2


def _cross_cmp(p: IntPoint, q: IntPoint) -> int:
    """同じ半平面の中で、q が p より反時計回り側なら負。O(1)"""
    return p[1] * q[0] - p[0] * q[1]


def make_arg_cmp(
    start: IntPoint = (1, 0), closed: bool = True
) -> Callable[[IntPoint, IntPoint], int]:
    """偏角の比較関数を作る。arg_sort(points, start, closed) と同じ順序になる。O(1)

    start: 始線の向き（原点以外の整数ベクトル）。ここから反時計回りに並べる。
    closed: True なら始線ちょうどの点を先頭に、False なら末尾に置く。
    原点は常に先頭に来る。偏角が等しい点どうしは cmp が0を返す。
    戻り値は cmp_sort.sort_by_cmp や array_binary_search.lower_bound などに渡せる。

    使い方:
        # atan2 と同じ (-π, π] の順（-x 方向から始めて、-x 方向ちょうどの点は末尾）
        cmp = make_arg_cmp((-1, 0), closed=False)

    https://github.com/yasyasyu/local-lib/blob/master/arg_sort.py
    """
    dx, dy = start

    def cmp(p: IntPoint, q: IntPoint) -> int:
        gp = _arg_group(p, dx, dy, closed)
        gq = _arg_group(q, dx, dy, closed)
        if gp != gq:
            return gp - gq
        return _cross_cmp(p, q)

    return cmp


# +x 方向から反時計回り（[0, 2π)）の偏角の比較関数。arg_sort(points) と同じ順序。O(1)
#
# 使い方:
#     a = arg_sort(points)
#     # 偏角が (1, 1) 以上 (-1, 1) 未満（[π/4, 3π/4)）の点の個数
#     lower_bound(a, (-1, 1), arg_cmp) - lower_bound(a, (1, 1), arg_cmp)
#
# https://github.com/yasyasyu/local-lib/blob/master/arg_sort.py
arg_cmp = make_arg_cmp()


def arg_sort(
    points: Iterable[IntPoint], start: IntPoint = (1, 0), closed: bool = True
) -> list[IntPoint]:
    """点を偏角の昇順に並べた新しいリストを返す（安定ソート、整数座標のみで誤差なし）。O(N log N)

    points: 点 (x, y) のリスト。中心が原点でないときは、(x - cx, y - cy) にしてから渡す。
    start: 始線の向き（原点以外の整数ベクトル）。ここから反時計回りに並べる。
    closed: True なら始線ちょうどの点を先頭に、False なら末尾に置く。
    原点は先頭に置く。偏角が等しい点どうしは、入力の順番のまま並ぶ。
    Pythonの整数はオーバーフローしないが、座標の絶対値が 2 * 10**9 程度を超えると
    外積が64bitに収まらず、PyPyでは多倍長整数になって遅くなる。

    使い方:
        arg_sort([(0, -1), (-1, 0), (1, 1), (1, 0)])
        # [(1, 0), (1, 1), (-1, 0), (0, -1)]

        # 偏角が等しい点は原点に近い順にしたい: 先に距離でソートしておく（安定なので順番が保たれる）
        arg_sort(sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1]))

        # (0, 1) の向きから始める
        arg_sort(points, start=(0, 1))

    https://github.com/yasyasyu/local-lib/blob/master/arg_sort.py
    """
    dx, dy = start
    groups: list[list[IntPoint]] = [[], [], []]
    for p in points:
        groups[_arg_group(p, dx, dy, closed)].append(p)
    # 比較関数の中で半平面を判定するより、先に半平面ごとに分けてから外積だけでソートする方が速い
    return (
        groups[0]
        + sort_by_cmp(groups[1], _cross_cmp)
        + sort_by_cmp(groups[2], _cross_cmp)
    )
