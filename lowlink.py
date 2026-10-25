class LowLink:
    """lowlink を求め、無向グラフの橋と関節点を列挙する（再帰を使わない DFS）。O(N + M)

    橋: 取り除くと連結成分が増える辺。関節点: 取り除く（つながる辺ごと）と連結成分が増える頂点。
    多重辺・自己ループがあってもよい（多重辺は橋にならない）。グラフは非連結でもよい。

    使い方:
        # 0 - 1 - 2 - 0 の三角形に、2 - 3 の辺をつけたグラフ
        edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
        ll = LowLink(4, edges)
        ll.bridges               # [3]（edges[3] = (2, 3) が橋）
        ll.articulation_points   # [2]

    https://github.com/yasyasyu/local-lib/blob/master/lowlink.py
    """

    def __init__(self, n: int, edges: list[tuple[int, int]]) -> None:
        """頂点数 n、辺のリスト edges の無向グラフについて求める。O(N + M)"""
        adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]  # (行き先, 辺の番号)
        for i, (u, v) in enumerate(edges):
            adj[u].append((v, i))
            adj[v].append((u, i))

        # ord[v]: DFS で訪れた順番。low[v]: v の部分木から、後退辺を高々1本使って行ける ord の最小値
        self.ord = [-1] * n
        self.low = [-1] * n
        self.bridges: list[int] = []  # 橋の辺の番号
        is_articulation = [False] * n
        parent = [-1] * n
        parent_edge = [-1] * n  # 親から来た辺の番号（多重辺を区別するため、頂点でなく辺で持つ）
        it = [0] * n  # 次に見る adj[v] の位置
        k = 0
        for root in range(n):
            if self.ord[root] != -1:
                continue
            self.ord[root] = self.low[root] = k
            k += 1
            root_children = 0
            stack = [root]
            while stack:
                v = stack[-1]
                if it[v] < len(adj[v]):
                    to, eid = adj[v][it[v]]
                    it[v] += 1
                    if eid == parent_edge[v]:
                        continue
                    if self.ord[to] == -1:
                        # 木辺: to へ降りる
                        parent[to] = v
                        parent_edge[to] = eid
                        self.ord[to] = self.low[to] = k
                        k += 1
                        stack.append(to)
                    elif self.ord[to] < self.low[v]:
                        # 後退辺
                        self.low[v] = self.ord[to]
                    continue
                # v の子をすべて見終わった: 親 p へ戻る
                stack.pop()
                p = parent[v]
                if p == -1:
                    continue
                if self.low[v] < self.low[p]:
                    self.low[p] = self.low[v]
                if self.ord[p] < self.low[v]:
                    self.bridges.append(parent_edge[v])
                if p == root:
                    root_children += 1
                elif self.ord[p] <= self.low[v]:
                    is_articulation[p] = True
            if root_children >= 2:
                is_articulation[root] = True

        self.bridges.sort()
        self.articulation_points = [v for v in range(n) if is_articulation[v]]
