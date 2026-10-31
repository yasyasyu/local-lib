from collections import deque


def zero_one_bfs(G: list[list[tuple[int, int]]], start: int) -> list[float]:
    """辺の重みが 0 か 1 のグラフの単一始点最短路（0-1 BFS）。O(N + M)

    :param G: 隣接リスト。G[u] = [(v, cost), ...]（cost は 0 か 1）。dijkstra.py と同じ形。

    重み0の辺は deque の先頭に、重み1の辺は末尾に積むことで、ダイクストラ法の log を消している。

    使い方::

        G = [[] for _ in range(N)]
        G[u].append((v, 0))   # 重み0の辺
        G[u].append((w, 1))   # 重み1の辺

        dist = zero_one_bfs(G, 0)
        # dist[v]: start から v への最短距離（到達できない場合は float("inf")）

    https://github.com/yasyasyu/local-lib/blob/master/zero_one_bfs.py
    """
    dist = [float("inf")] * len(G)
    dist[start] = 0
    dq = deque([start])
    while dq:
        v = dq.popleft()
        d = dist[v]
        for u, cost in G[v]:
            nd = d + cost
            if nd < dist[u]:
                dist[u] = nd
                if cost == 0:
                    dq.appendleft(u)
                else:
                    dq.append(u)
    return dist
