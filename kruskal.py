from .union_find import UnionFind


def kruskal(
    edges: list[tuple[int, int, int]], N: int
) -> tuple[int, list[tuple[int, int, int]]]:
    """クラスカル法による最小全域木（MST）

    edges: 辺のリスト [(cost, u, v), ...]
    N: 頂点数

    使い方:
        edges = [(1, 0, 1), (2, 1, 2), (3, 0, 2)]
        total_cost, used_edges = kruskal(edges, 3)
        # total_cost: MSTの総コスト
        # used_edges: MSTに使われた辺のリスト [(cost, u, v), ...]
        # グラフが連結でない場合は最小全域森になる

    https://github.com/yasyasyu/local-lib/blob/master/kruskal.py
    """
    uf = UnionFind(N)
    total_cost = 0
    used_edges = []
    for cost, u, v in sorted(edges):
        if uf.same(u, v):
            continue
        uf.merge(u, v)
        total_cost += cost
        used_edges.append((cost, u, v))
    return total_cost, used_edges
