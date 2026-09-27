from .doubling import Doubling


class LCA:
    """最小共通祖先（LCA）をダブリングで求めるデータ構造

    使い方:
        # 0 -> 1, 2 ; 1 -> 3, 4 という木（無向辺として渡す）
        G = [[1, 2], [0, 3, 4], [0], [1], [1]]
        lca = LCA(G, root=0)
        lca.query(3, 4)      # 1
        lca.depth[3]         # 頂点3の深さ -> 2
        lca.distance(3, 4)   # 3と4の間の距離（辺数）-> 2

    https://github.com/yasyasyu/local-lib/blob/master/lca.py
    """

    def __init__(self, G: list[list[int]], root: int = 0) -> None:
        """木Gを根rootで構築する。O(N log N)"""
        N = len(G)
        self.depth = [-1] * N
        parent = [0] * N
        parent[root] = root
        self.depth[root] = 0
        stack = [root]
        while stack:
            v = stack.pop()
            for to in G[v]:
                if self.depth[to] != -1:
                    continue
                self.depth[to] = self.depth[v] + 1
                parent[to] = v
                stack.append(to)

        self.doubling = Doubling(N, N, lambda x: parent[x])

    def query(self, u: int, v: int) -> int:
        """頂点uとvの最小共通祖先を返す。O(log N)"""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # 深い方のuを、vと同じ深さまで持ち上げる
        u = self.doubling.get(u, self.depth[u] - self.depth[v])
        if u == v:
            return u

        # 2^i個上の祖先が異なる間だけ、大きいiから順に両方を持ち上げる。
        # 最後にu, vはLCAの直下の子になっている
        table = self.doubling.doubling_table
        for i in range(len(table) - 1, -1, -1):
            if table[i][u] != table[i][v]:
                u, v = table[i][u], table[i][v]

        return table[0][u]

    def distance(self, u: int, v: int) -> int:
        """頂点uとvの間の距離（辺数）を返す。O(log N)"""
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.query(u, v)]
