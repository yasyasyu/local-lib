from .tree_order import tree_order


class HLD:
    """HL 分解（重軽分解）。木のパスを O(log N) 個の連続区間に分け、パス上のクエリを列のクエリにする

    各頂点 v に列の位置 index(v) を割り当てる。どの頂点から根へのパスも O(log N) 個の連続区間になり、
    部分木は1つの連続区間になる。ac-library-python の SegTree などと組み合わせて使う。
    パスの区間は順番を考えずに返すので、演算は可換であること（和・min・max など）。

    使い方:
        hld = HLD(G, root=0)
        seg = SegTree(op, e, [A[hld.order[i]] for i in range(N)])  # 列の位置 i には頂点 order[i] の値

        # u-v パス上の頂点の値の集約
        res = e
        for l, r in hld.path(u, v):
            res = op(res, seg.prod(l, r))

        seg.set(hld.index(v), x)              # 頂点 v の値を x にする
        l, r = hld.subtree(v)                 # v の部分木は列の [l, r)
        hld.lca(u, v), hld.dist(u, v)

        # 辺に値を持たせるときは、辺 (親, 子) の値を子の位置に置き、edge=True で LCA を除く
        hld.path(u, v, edge=True)

    https://github.com/yasyasyu/local-lib/blob/master/hld.py
    """

    def __init__(self, G: list[list[int]], root: int = 0) -> None:
        """木の隣接リスト G から構築する（再帰を使わない）。O(N)"""
        N = len(G)
        bfs, parent = tree_order(G, root)
        self.parent = parent
        self.depth = [0] * N
        for v in bfs[1:]:
            self.depth[v] = self.depth[parent[v]] + 1
        self.size = [1] * N
        heavy = [-1] * N  # heavy[v]: 部分木が最も大きい子
        for v in reversed(bfs[1:]):
            p = parent[v]
            self.size[p] += self.size[v]
        for v in bfs[1:]:
            p = parent[v]
            if heavy[p] == -1 or self.size[v] > self.size[heavy[p]]:
                heavy[p] = v

        # heavy な子を先に訪れる DFS の行きがけ順に、列の位置を割り当てる
        # （heavy な子は親のすぐ次の位置になり、heavy path が連続区間になる）
        self.head = [0] * N  # head[v]: v を含む heavy path の一番上の頂点
        self._index = [0] * N
        self.order = [0] * N  # order[i]: 列の位置 i にある頂点
        stack = [root]
        self.head[root] = root
        t = 0
        while stack:
            v = stack.pop()
            self._index[v] = t
            self.order[t] = v
            t += 1
            p = parent[v]
            for u in G[v]:
                if u != p and u != heavy[v]:
                    self.head[u] = u
                    stack.append(u)
            if heavy[v] != -1:
                self.head[heavy[v]] = self.head[v]
                stack.append(heavy[v])  # 最後に積むので、次に取り出される

    def index(self, v: int) -> int:
        """頂点 v の列の位置を返す。O(1)"""
        return self._index[v]

    def lca(self, u: int, v: int) -> int:
        """u と v の最小共通祖先を返す。O(log N)"""
        head = self.head
        idx = self._index
        while head[u] != head[v]:
            if idx[head[u]] > idx[head[v]]:
                u = self.parent[head[u]]
            else:
                v = self.parent[head[v]]
        return u if idx[u] < idx[v] else v

    def dist(self, u: int, v: int) -> int:
        """u と v の距離（辺の本数）を返す。O(log N)"""
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def ancestor(self, v: int, k: int) -> int:
        """v から根の方へ k 回上った頂点を返す（k が深さを超えたら -1）。O(log N)"""
        if k > self.depth[v]:
            return -1
        head = self.head
        idx = self._index
        while True:
            h = head[v]
            up = idx[v] - idx[h]  # v から heavy path の一番上まで上れる回数
            if k <= up:
                return self.order[idx[v] - k]
            k -= up + 1
            v = self.parent[h]

    def path(self, u: int, v: int, edge: bool = False) -> list[tuple[int, int]]:
        """u-v パスを、列の半開区間 [l, r) のリストに分けて返す（順番は不定）。O(log N)

        edge=True なら LCA の位置を除く（辺の値を子の位置に置いているとき用）。
        """
        head = self.head
        idx = self._index
        res = []
        while head[u] != head[v]:
            if idx[head[u]] < idx[head[v]]:
                u, v = v, u
            res.append((idx[head[u]], idx[u] + 1))
            u = self.parent[head[u]]
        if idx[u] > idx[v]:
            u, v = v, u
        # u が LCA
        l = idx[u] + (1 if edge else 0)
        if l <= idx[v]:
            res.append((l, idx[v] + 1))
        return res

    def subtree(self, v: int, edge: bool = False) -> tuple[int, int]:
        """v の部分木を表す列の半開区間 [l, r) を返す。edge=True なら v 自身の位置を除く。O(1)"""
        l = self._index[v]
        return (l + (1 if edge else 0), l + self.size[v])
