import sys


class StronglyConnectedComponents:
    """強連結成分分解（Kosaraju法）。O(N + M)（Nは頂点数、Mは辺数）

    使い方::

        scc = StronglyConnectedComponents(4)
        scc.add_edge(0, 1)
        scc.add_edge(1, 0)
        scc.add_edge(2, 3)
        groups = scc.components()  # 例: [[0, 1], [2], [3]]（トポロジカル順）

    https://github.com/yasyasyu/local-lib/blob/master/strongly_connected_components.py
    """

    def __init__(self, n: int) -> None:
        """頂点数nのグラフを作る。O(n)"""
        self.n = n
        self.edge: list[list[int]] = [[] for _ in range(n)]
        self.reverse_edge: list[list[int]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int) -> None:
        """有向辺u->vを追加する。O(1)"""
        self.edge[u].append(v)
        self.reverse_edge[v].append(u)

    def _postorder(self) -> list[int]:
        """1回目のDFSで帰りがけ順を求める。O(N + M)"""
        postorder: list[int] = []
        visited = [False] * self.n

        def dfs(v: int) -> None:
            visited[v] = True
            for to in self.edge[v]:
                if visited[to]:
                    continue
                dfs(to)
            postorder.append(v)

        for v in range(self.n):
            if visited[v]:
                continue
            dfs(v)

        return postorder

    def _collect(self, order: list[int]) -> list[list[int]]:
        """逆辺グラフをorderの順にDFSし、強連結成分に分ける。O(N + M)"""
        visited = [False] * self.n
        groups: list[list[int]] = []

        def dfs(v: int, group: list[int]) -> None:
            visited[v] = True
            group.append(v)
            for to in self.reverse_edge[v]:
                if visited[to]:
                    continue
                dfs(to, group)

        for v in order:
            if visited[v]:
                continue
            group: list[int] = []
            dfs(v, group)
            groups.append(group)

        return groups

    def components(self) -> list[list[int]]:
        """強連結成分のリストをトポロジカル順で返す。O(N + M)"""
        sys.setrecursionlimit(max(sys.getrecursionlimit(), self.n * 2 + 10))
        postorder = self._postorder()
        return self._collect(postorder[::-1])
