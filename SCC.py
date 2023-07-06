class SCC:
    def __init__(self, n):
        self.n = n
        self.edge = [[] for _ in range(n)]
        self.redge = [[] for _ in range(n)]

    def connect(self, frm, to):
        self.edge[frm].append(to)
        self.redge[to].append(frm)

    def dfs1(self):
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

    def dfs2(self, reveseorder):
        bef = [False for _ in range(self.n)]
        grps = []

        def _dfs(frm, grp):
            bef[frm] = True
            grp.append(frm)
            for to in self.redge[frm]:
                if bef[to]:
                    continue
                _dfs(to, grp)

        for v in reveseorder:
            grp = []
            if bef[v]:
                continue
            _dfs(v, grp)
            grps.append(grp)

        return grps

    def solve(self):
        order = self.dfs1()
        grps = self.dfs2(order[::-1])

        return grps
