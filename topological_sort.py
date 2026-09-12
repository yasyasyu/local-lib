from collections import deque


def topological_sort(es):
    """
    es : 有向グラフ（隣接リスト。es[u]はuから出る辺の行き先のリスト）

    使い方:
        n, m = map(int, input().split())
        es = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            es[u - 1].append(v - 1)

        order = topological_sort(es)
    """
    V = len(es)
    deg = [0] * V
    for i in range(V):
        for e in es[i]:
            deg[e] += 1
    d = deque()
    for i, deg_i in enumerate(deg):
        if deg_i == 0:
            d.append(i)
    order = []
    while d:
        v = d.popleft()
        order.append(v)
        for i in es[v]:
            deg[i] -= 1
            if deg[i] == 0:
                d.append(i)

    return order
