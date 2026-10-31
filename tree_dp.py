from typing import Callable, TypeVar

from .tree_order import tree_order

T = TypeVar("T")


def tree_dp(
    G: list[list[int]],
    op: Callable[[T, T], T],
    e: T,
    add_vertex: Callable[[T, int], T],
    add_edge: Callable[[T, int, int], T] | None = None,
    root: int = 0,
) -> list[T]:
    """木DP。根を1つ決めて、すべての頂点について、その頂点を根とする部分木の値を返す。O(N)

    :param G: 木の隣接リスト（無向）。
    :param op: 子から来た値をまとめる演算 op(a, b)（可換モノイド。足し算・max など）。
    :param e: op の単位元。
    :param add_vertex: add_vertex(x, v)。子からの値をまとめた x に頂点 v を足して、v を根とする部分木の値にする。
    :param add_edge: add_edge(x, frm, to)。部分木の値 x を、辺 frm -> to を通して親 to へ渡す値にする。省略すると x のまま。
    :param root: 根。
    :return: dp[v] は v を根とする部分木の値。木全体の値は dp[root]。
    :rtype: list[T]

    引数は rerooting_tree_dp.py と同じなので、全部の頂点を根にしたくなったら rerooting_tree_dp に差し替えられる。

    再帰を使わないので、深い木でも使える。

    使い方::

        # 部分木の大きさ
        size = tree_dp(G, lambda a, b: a + b, 0, lambda x, v: x + 1)

        # 高さ（葉は 0。e = -1 で葉が 0 になる）
        height = tree_dp(G, max, -1, lambda x, v: x + 1)

        # 最大独立集合の大きさ。値は (v を選ばないときの最大, v を選ぶときの最大)
        dp = tree_dp(
            G,
            op=lambda a, b: (a[0] + b[0], a[1] + b[1]),
            e=(0, 0),
            add_vertex=lambda x, v: (x[0], x[1] + 1),
            add_edge=lambda x, frm, to: (max(x), x[0]),  # 親を選ばないなら子は自由、選ぶなら子は選ばない
        )
        ans = max(dp[0])

        # 直径。値は (高さ, 部分木の中の最長パスの長さ)。単位元が作りにくいので e = None にする
        def merge_longest(a, b):
            if a is None:
                return b
            a_height, a_length = a
            b_height, b_length = b
            return max(a_height, b_height), max(a_length, b_length, a_height + b_height)

        _, D = tree_dp(
            G,
            op=merge_longest,
            e=None,
            add_vertex=lambda x, v: merge_longest(x, (0, 0)),  # 頂点 v 自身: 高さ 0、最長パス 0
            add_edge=lambda x, frm, to: (x[0] + 1, x[1]),  # 親から見ると高さが 1 増える
        )[0]

        # 同じ色（C[v]）で距離がちょうど D（直径）の2頂点の組の数。組は2頂点の LCA で数える
        # 値は (高さ h, 深さ h にある頂点の色ごとの個数 Counter, 部分木の中の組の数)
        # 深さが h より浅い頂点は、この先どこと組んでも距離 D にならないので捨てる
        def merge_deepest(a, b):
            if a is None:
                return b
            a_height, a_colors, a_pairs = a
            b_height, b_colors, b_pairs = b
            pairs = a_pairs + b_pairs
            if len(a_colors) < len(b_colors):  # 色の少ないほうを b にして回す（マージテク）
                a_height, a_colors, b_height, b_colors = b_height, b_colors, a_height, a_colors
            # a の最も深い頂点と b の最も深い頂点の距離がちょうど D なら、同色の組を数える
            if a_height + b_height == D:
                pairs += sum(m * a_colors[k] for k, m in b_colors.items())
            if a_height > b_height:
                return a_height, a_colors, pairs
            if a_height < b_height:
                return b_height, b_colors, pairs
            for k, m in b_colors.items():
                a_colors[k] += m  # a_colors を書き換えるので、根以外の dp の値は壊れる
            return a_height, a_colors, pairs

        dp = tree_dp(
            G,
            op=merge_deepest,
            e=None,
            add_vertex=lambda x, v: merge_deepest(x, (0, Counter({C[v]: 1}), 0)),  # 頂点 v 自身
            add_edge=lambda x, frm, to: (x[0] + 1, x[1], x[2]),  # 親から見ると高さが 1 増える
        )
        _, _, ans = dp[0]

    定式化のヒント:

    - 「何を値に持てば、子たちの値から親の値が作れるか」を考える。足りなければタプルにして増やす。
      （直径: 高さだけでは部分木の中の最長パスがわからないので、(高さ, 最長パス) にする）
    - 2頂点の組を数える問題は、組を2頂点の LCA で数える。op(a, b) で「それまでに合わせた子たち a」と
      「新しい子 b」の間の組を数え、組の数も値に入れて足していく。
    - 頂点 v 自身も「子が1つ増えた」とみなして add_vertex(x, v) = op(x, v だけの値) と書くと、
      葉の場合や、v 自身が組の片方になる場合も同じ式で扱える。
    - 単位元が作りにくいときは e = None にして、op の先頭で「a が None なら b を返す」とする。
      tree_dp で None が来るのは op の左と add_vertex の x だけ。
      rerooting_tree_dp では op のどちらにも None が来るので、b が None の場合も扱う。
    - 組を作れない頂点は値から捨てて小さくする（同色の組の例: 一番深い頂点以外は捨てる）。
    - 値に Counter やリストを持つときは、op で小さいほうを大きいほうに足す（マージテク。全体 O(N log N)）。
      その場で書き換えると根以外の dp[v] は壊れるので、使うのは dp[root] だけにする。
      rerooting_tree_dp は同じ値を何度も使うので、書き換えるマージテクは使えない。

    https://github.com/yasyasyu/local-lib/blob/master/tree_dp.py
    """
    N = len(G)
    order, parent = tree_order(G, root)
    if add_edge is None:

        def add_edge(x: T, frm: int, to: int) -> T:
            return x

    # 葉から順に見る。dp[v] には、v を見る時点で子からの値がすべてまとまっている
    dp = [e] * N
    for v in reversed(order):
        dp[v] = add_vertex(dp[v], v)
        p = parent[v]
        if p != -1:
            dp[p] = op(dp[p], add_edge(dp[v], v, p))
    return dp
