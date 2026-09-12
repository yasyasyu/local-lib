import heapq


def dijkstra(G: list[list[tuple[int, int]]], start: int) -> list[float]:
    """単一始点最短路（ダイクストラ法、負の重みがない場合のみ使える）

    G: 隣接リスト。G[u] = [(v, cost), ...]
    start: 始点

    使い方:
        N, M = map(int, input().split())
        G = [[] for _ in range(N)]
        for _ in range(M):
            u, v, c = map(int, input().split())
            G[u].append((v, c))
            G[v].append((u, c))  # 無向グラフの場合

        dist = dijkstra(G, 0)
        # dist[v]: startからvへの最短距離（到達不可能な場合はfloat("inf")）

    https://github.com/yasyasyu/local-lib/blob/master/dijkstra.py
    """
    N = len(G)
    dist = [float("inf")] * N
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, v = heapq.heappop(pq)
        if dist[v] < d:
            continue
        for to, cost in G[v]:
            nd = d + cost
            if nd < dist[to]:
                dist[to] = nd
                heapq.heappush(pq, (nd, to))
    return dist
