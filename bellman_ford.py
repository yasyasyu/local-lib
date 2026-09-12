def bellman_ford(
    edges: list[tuple[int, int, int]], N: int, start: int
) -> list[float]:
    """単一始点最短路（ベルマンフォード法、負の重み・負閉路検出に対応）

    edges: 辺のリスト [(u, v, cost), ...]（有向辺。無向辺はu->vとv->uの両方を入れる）
    N: 頂点数
    start: 始点

    使い方:
        edges = [(0, 1, 3), (1, 2, -2), (2, 0, 1)]
        dist = bellman_ford(edges, 3, 0)
        # dist[v]: startからvへの最短距離
        # 到達不可能な頂点は float("inf")
        # 負閉路から到達可能な頂点は float("-inf")

    https://github.com/yasyasyu/local-lib/blob/master/bellman_ford.py
    """
    INF = float("inf")
    dist = [INF] * N
    dist[start] = 0
    for _ in range(N - 1):
        updated = False
        for u, v, cost in edges:
            if dist[u] == INF:
                continue
            if dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                updated = True
        if not updated:
            break

    # 負閉路上、及びそこから到達可能な頂点をすべて-infにする
    neg = [False] * N
    for _ in range(N):
        updated = False
        for u, v, cost in edges:
            if dist[u] == INF and not neg[u]:
                continue
            if neg[u] or dist[u] + cost < dist[v]:
                if not neg[v]:
                    neg[v] = True
                    updated = True
        if not updated:
            break

    for v in range(N):
        if neg[v]:
            dist[v] = float("-inf")

    return dist
