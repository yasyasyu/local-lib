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
        """頂点uとvの最小共通祖先を返す。"""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.doubling.get(u, self.depth[u] - self.depth[v])
        if u == v:
            return u

        ok, ng = 0, self.depth[u] + 1
        while ng - ok > 1:
            mid = (ok + ng) // 2
            if self.doubling.get(u, mid) != self.doubling.get(v, mid):
                ok = mid
            else:
                ng = mid

        return self.doubling.get(u, ng)

    def distance(self, u: int, v: int) -> int:
        """頂点uとvの間の距離（辺数）を返す。"""
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.query(u, v)]
