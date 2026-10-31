def tree_order(G: list[list[int]], root: int = 0) -> tuple[list[int], list[int]]:
    """根付き木の BFS 順と親を、再帰を使わずに求める。O(N)

    :param G: 木の隣接リスト（無向。G[u] は u と隣り合う頂点のリスト）。連結で閉路がないこと。
    :param root: 根。
    :return: (order, parent)
    :rtype: tuple[list[int], list[int]]

    - order: 根から近い順（BFS 順）の頂点のリスト。順に回すと親が子より先に、逆から回すと子が親より先に来る。
    - parent: parent[v] は v の親。parent[root] = -1。

    Python の再帰は遅く、深い木では再帰の上限にも引っかかるので、木の DP はこれで書く。

    使い方::

        order, parent = tree_order(G, 0)

        # 深さ（根から順に）
        depth = [0] * N
        for v in order[1:]:
            depth[v] = depth[parent[v]] + 1

        # 部分木の大きさ（葉から順に）
        size = [1] * N
        for v in reversed(order[1:]):
            size[parent[v]] += size[v]

    https://github.com/yasyasyu/local-lib/blob/master/tree_order.py
    """
    parent = [-1] * len(G)
    order = [root]
    for v in order:  # 走査中に order が伸びていくので、BFS になる
        p = parent[v]
        for u in G[v]:
            if u != p:
                parent[u] = v
                order.append(u)
    return order, parent
