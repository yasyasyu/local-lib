from typing import Callable, TypeVar

from .tree_order import tree_order

T = TypeVar("T")


def rerooting_tree_dp(
    G: list[list[int]],
    op: Callable[[T, T], T],
    e: T,
    add_vertex: Callable[[T, int], T],
    add_edge: Callable[[T, int, int], T] | None = None,
) -> list[T]:
    """全方位木DP。すべての頂点について、その頂点を根にしたときの木全体の値を返す。O(N)

    G: 木の隣接リスト（無向）。
    op, e: 子から来た値をまとめる演算と単位元（可換モノイド。足し算・max など）。
    add_vertex(x, v): 子からの値をまとめた x に頂点 v を足して、v を根とする部分木の値にする。
    add_edge(x, frm, to): 部分木の値 x を、辺 frm -> to を通して親 to へ渡す値にする。省略すると x のまま。
    戻り値 ans: ans[v] は v を根にしたときの値（= add_vertex(すべての隣からの値, v)）。
    再帰を使わないので、深い木でも使える。

    使い方:
        # 各頂点から他のすべての頂点への距離の和（ABC220 F）。値は (頂点数, 距離の和)
        ans = rerooting_tree_dp(
            G,
            op=lambda a, b: (a[0] + b[0], a[1] + b[1]),
            e=(0, 0),
            add_vertex=lambda x, v: (x[0] + 1, x[1]),
            add_edge=lambda x, frm, to: (x[0], x[1] + x[0]),  # 辺を1本通ると、全頂点の距離が1増える
        )
        dist_sum = [s for _, s in ans]

        # 各頂点から一番遠い頂点までの距離（辺の重みは W[(frm, to)]）
        ans = rerooting_tree_dp(G, max, 0, lambda x, v: x, lambda x, frm, to: x + W[(frm, to)])

    https://github.com/yasyasyu/local-lib/blob/master/rerooting_tree_dp.py
    """
    N = len(G)
    order, parent = tree_order(G, 0)
    if add_edge is None:

        def add_edge(x: T, frm: int, to: int) -> T:
            return x

    # 1回目（葉から根へ）: contrib[v] = v の部分木の値を、親へ渡す形にしたもの
    acc = [e] * N  # acc[v]: v の子からの値をまとめたもの
    contrib = [e] * N
    for v in reversed(order):
        p = parent[v]
        if p != -1:
            x = add_edge(add_vertex(acc[v], v), v, p)
            contrib[v] = x
            acc[p] = op(acc[p], x)

    # 2回目（根から葉へ）: up[v] = 親の側（v の部分木以外）を、v へ渡す形にしたもの
    up = [e] * N
    ans = [e] * N
    for v in order:
        p = parent[v]
        children = [u for u in G[v] if u != p]
        k = len(children)
        # suffix[i] = children[i:] からの値をまとめたもの
        suffix = [e] * (k + 1)
        for i in range(k - 1, -1, -1):
            suffix[i] = op(contrib[children[i]], suffix[i + 1])
        ans[v] = add_vertex(op(up[v], suffix[0]), v)
        # prefix = 親の側と children[:i] からの値をまとめたもの。子 c に渡すのは「c 以外すべて」
        prefix = up[v]
        for i, c in enumerate(children):
            up[c] = add_edge(add_vertex(op(prefix, suffix[i + 1]), v), v, c)
            prefix = op(prefix, contrib[c])
    return ans
