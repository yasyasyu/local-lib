class UnionFind:
    """Union-Find（素集合データ構造）の改造用ベース

    普通のUnion-Findとして使うなら`atcoder.dsu.DSU`を使う。このクラスは、Union-Findに
    情報を載せたり動きを変えたりする問題で、コピーして改造する土台として置いている。

    ただし、次の2つは一般化したクラスがあるので、まずそちらで足りないかを考える:
        - 集合ごとの値（下の方針1・2）: monoid_union_find.py の MonoidUnionFind（opとvを渡す）
        - 要素間の重み（下の方針4）: potential_union_find.py の PotentialUnionFind（群をop / inv / eで渡す）
    そのため、改造しやすいように処理を最小限にし、改造する場所に「改造ポイント」のコメントを付けている。

    経路圧縮とunion by rankにより、find / merge / sameはならしO(α(N))（実質定数）。

    改造の方針:
        基本は「集合の情報は根にだけ持ち、merge で子になる側の根の情報を親になる側の根へまとめる」。
        根以外の要素が持つ値は、その要素が根だった頃の古い値なので読まないこと。
        取得は必ず data[self.find(x)] の形で行う。

        1. 集合ごとの値（要素数・和・最小値・最大値・辺の本数など）を持つ
           __init__で配列を用意し、mergeの改造ポイント(B)で「data[y] = op(data[y], data[x])」とする。
           例: 要素数ならsize[y] += size[x]、和ならtotal[y] += total[x]。
           要素数でunion by sizeにしたい場合は、rankの代わりにsizeを比べてもよい（計算量は同じ）。

        2. 同じ集合内に辺を張ったことを数える（閉路判定、辺数 = 頂点数 - 1 で木かどうか など）
           mergeの改造ポイント(A)（x == yで既に同じ集合のとき）で、edges[x] += 1のように記録する。
           (B)ではedges[y] += edges[x] + 1とする（+1は今回張った辺）。

        3. 集合の要素リストそのものを持つ（マージテク）
           members[y].extend(members[x])を(B)で行う。rankが大きい方（=木が大きい方）に
           小さい方を足すとは限らないので、要素数の小さい方を大きい方へ足すようにsizeで比べ直すこと。
           そうすれば全体でO(N log N)。

        4. 要素間の差（ポテンシャル・重み）を持つ
           findの改造ポイント(C)で、親を根に付け替える前に「weight[x] += weight[元の親]」とする
           （再帰で元の親を先に根へ付け替えておけば、weight[元の親]は元の親から根までの差になる）。
           任意の群で一般化した完成版がpotential_union_find.py。二部グラフ判定・偶奇の管理は、重みをmod 2で持てばよい。

        5. mergeを取り消せるようにする（オフラインの辺削除、分割統治など）
           経路圧縮をやめ（findの(C)を消して親を辿るだけにする）、mergeで書き換える前の値を履歴に積む。
           完成版はrollback_union_find.pyを参照。この場合findはO(log N)になる。

    使い方:
        uf = UnionFind(5)
        uf.merge(0, 1)
        uf.same(0, 1)   # True
        uf.groups()     # [[0, 1], [2], [3], [4]]

    https://github.com/yasyasyu/local-lib/blob/master/union_find.py
    """

    def __init__(self, N) -> None:
        """要素数Nで初期化する。O(N)"""
        self.N = N
        self.parent = [-1] * N
        self.rank = [-1] * N
        # 改造ポイント: 集合ごとの値はここで用意する（例: self.size = [1] * N）

    def find(self, x):
        """xの属する集合の代表元を返す。ならしO(α(N))"""
        if self.parent[x] == -1:
            return x
        root = self.find(self.parent[x])
        # 改造ポイント(C): ここではself.parent[x]はまだ元の親を指している。
        # 元の親はすでに根に直結しているので、元の親の値を使ってxの値を更新してから付け替える
        self.parent[x] = root
        return root

    def merge(self, x, y):
        """xとyの属する集合を併合する。ならしO(α(N))"""
        x = self.find(x)
        y = self.find(y)
        if x == y:
            # 改造ポイント(A): 既に同じ集合だったとき（閉路になる辺など）の処理
            return
        if self.rank[x] > self.rank[y]:
            x, y = y, x
        elif self.rank[x] == self.rank[y]:
            self.rank[y] += 1

        self.parent[x] = y
        # 改造ポイント(B): 根xの集合が根yの集合に吸収された。xの情報をyにまとめる

    def same(self, x, y):
        """xとyが同じ集合に属するかを返す。ならしO(α(N))"""
        return self.find(x) == self.find(y)

    def groups(self):
        """集合ごとの要素のリストを返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.find(i)].append(i)

        return list(filter(lambda r: r, G))
