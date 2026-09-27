import sys


class SCC:
    """強連結成分分解（Kosaraju法）。O(N + M)（Nは頂点数、Mは辺数）

    使い方:
        scc = SCC(4)
        scc.connect(0, 1)
        scc.connect(1, 0)
        scc.connect(2, 3)
        groups = scc.solve()  # 例: [[0, 1], [2], [3]]（トポロジカル順）

    https://github.com/yasyasyu/local-lib/blob/master/scc.py
    """

    def __init__(self, n):
        """頂点数nのグラフを作る。O(n)"""
        self.n = n
        self.edge = [[] for _ in range(n)]
        self.redge = [[] for _ in range(n)]

    def connect(self, frm, to):
        """有向辺frm->toを追加する。O(1)"""
        self.edge[frm].append(to)
        self.redge[to].append(frm)

    def dfs1(self):
        """1回目のDFSで帰りがけ順を求める。O(N + M)"""
        backorder = []
        bef = [False for _ in range(self.n)]

        def _dfs(frm):
            bef[frm] = True
            for to in self.edge[frm]:
                if bef[to]:
                    continue
                _dfs(to)
            backorder.append(frm)

        for v in range(self.n):
            if bef[v]:
                continue
            _dfs(v)

        return backorder

    def dfs2(self, reverse_order):
        """逆辺グラフを帰りがけ順の逆順にDFSし、強連結成分に分ける。O(N + M)"""
        bef = [False for _ in range(self.n)]
        grps = []

        def _dfs(frm, grp):
            bef[frm] = True
            grp.append(frm)
            for to in self.redge[frm]:
                if bef[to]:
                    continue
                _dfs(to, grp)

        for v in reverse_order:
            grp = []
            if bef[v]:
                continue
            _dfs(v, grp)
            grps.append(grp)

        return grps

    def solve(self):
        """強連結成分のリストをトポロジカル順で返す。O(N + M)"""
        sys.setrecursionlimit(max(sys.getrecursionlimit(), self.n * 2 + 10))
        order = self.dfs1()
        grps = self.dfs2(order[::-1])

        return grps
