def warshall_floyd(G: list[list[float]]) -> list[list[float]]:
    """全点対最短路（ワーシャルフロイド法）

    G: 隣接行列。G[i][j]は辺(i,j)の重み、辺が無い場合はfloat("inf")、G[i][i]は0。
       負の重みがあってもよいが、負閉路がある場合の結果は保証しない。

    使い方:
        INF = float("inf")
        G = [
            [0, 3, INF],
            [3, 0, 1],
            [INF, 1, 0],
        ]
        dist = warshall_floyd(G)
        # dist[i][j]: iからjへの最短距離（到達不可能な場合はfloat("inf")）

    https://github.com/yasyasyu/local-lib/blob/master/warshall_floyd.py
    """
    N = len(G)
    dist = [row[:] for row in G]
    for k in range(N):
        dist_k = dist[k]
        for i in range(N):
            dist_i = dist[i]
            if dist_i[k] == float("inf"):
                continue
            dik = dist_i[k]
            for j in range(N):
                if dik + dist_k[j] < dist_i[j]:
                    dist_i[j] = dik + dist_k[j]
    return dist
