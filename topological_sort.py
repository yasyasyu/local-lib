from collections import deque


def topological_sort(directed_graph: list[list[int]]) -> list[int]:
    """トポロジカルソート（Kahn法）。O(N + M)（Nは頂点数、Mは辺数）

    閉路がある場合、閉路に関わる頂点は結果に含まれない（len(order) < Nで閉路の有無を判定できる）。

    es : 有向グラフ（隣接リスト。es[u]はuから出る辺の行き先のリスト）

    使い方::

        n, m = map(int, input().split())
        es = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            es[u - 1].append(v - 1)

        order = topological_sort(es)

    https://github.com/yasyasyu/local-lib/blob/master/topological_sort.py
    """
    V = len(directed_graph)
    deg = [0] * V
    for i in range(V):
        for e in directed_graph[i]:
            deg[e] += 1
    d: deque[int] = deque()
    for i, deg_i in enumerate(deg):
        if deg_i == 0:
            d.append(i)
    order: list[int] = []
    while d:
        v = d.popleft()
        order.append(v)
        for i in directed_graph[v]:
            deg[i] -= 1
            if deg[i] == 0:
                d.append(i)

    return order
