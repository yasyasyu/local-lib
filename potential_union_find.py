import typing


class PotentialUnionFind:
    """重み付きUnion-Find（ポテンシャル付き素集合データ構造）。重みは任意の群で持てる

    unite(a, b, d) で「aから見たbの重みがd」という関係を追加し、dist(a, b) でそれを求める。
    重みの群は op（演算）・inv（逆元）・e（単位元）で指定する。省略すると整数の足し算になり、
    unite(a, b, d) は「potential[b] - potential[a] = d」を表す。
    一般の群では「aから見たbの重み」を op(inv(potential[a]), potential[b]) と定義する
    （potential[x]は根から見たxの重み）。つまり op(potential[a], d) == potential[b]。

    連結判定は same() ではなく dist(a, b) != INF で行う（INFはinfで指定、既定は10**18）。
    unite は関係と矛盾するかを調べないので、矛盾の検出が必要なら先に dist で確かめること。

    経路圧縮とunion by sizeにより、root / dist / unite / sizeはならしO(α(N))（実質定数）。

    使い方:
        uf = PotentialUnionFind(3)
        uf.unite(0, 1, 5)  # potential[1] - potential[0] = 5
        uf.dist(0, 1)      # 5
        uf.dist(1, 2)      # 未連結ならINF

        # XORの重み（「a xor b = d」の関係を管理する）
        uf = PotentialUnionFind(3, op=lambda a, b: a ^ b, inv=lambda a: a, e=0)

        # 二部グラフ判定・偶奇の管理（mod 2の足し算）
        uf = PotentialUnionFind(3, op=lambda a, b: a ^ b, inv=lambda a: a, e=0)
        uf.unite(0, 1, 1)  # 0と1は異なる色
        uf.dist(0, 1) == 1

        # 非可換な群（例: x -> a*x + b のアフィン変換を(a, b)で表し、先にfを施してからgを施す合成をop(f, g)とする）
        MOD = 998244353
        uf = PotentialUnionFind(
            3,
            op=lambda f, g: (f[0] * g[0] % MOD, (g[0] * f[1] + g[1]) % MOD),
            inv=lambda f: (pow(f[0], -1, MOD), -pow(f[0], -1, MOD) * f[1] % MOD),
            e=(1, 0),
        )

    https://github.com/yasyasyu/local-lib/blob/master/potential_union_find.py
    """

    def __init__(
        self,
        N: int,
        inf: typing.Any = 10**18,
        op: typing.Callable[[typing.Any, typing.Any], typing.Any] = lambda a, b: a + b,
        inv: typing.Callable[[typing.Any], typing.Any] = lambda a: -a,
        e: typing.Any = 0,
    ) -> None:
        """要素数Nで初期化する。O(N)"""
        self.N = N
        # parent[x] < 0 のときxは根で、-parent[x]がその集合の要素数
        self.parent = [-1] * N
        # potential[x]: 親から見たxの重み（root()を呼んだ直後は根から見たxの重み）
        self.potential = [e] * N
        self.INF = inf
        self._op = op
        self._inv = inv
        self._e = e

    def root(self, a: int) -> int:
        """aの属する集合の根を返す（経路圧縮しつつ、重みを根から見た値に更新する）。ならしO(α(N))"""
        path = []
        while self.parent[a] >= 0:
            path.append(a)
            a = self.parent[a]
        r = a
        # 根に近い方から順に、根から見た重みを積み上げていく
        acc = self._e
        for v in reversed(path):
            acc = self._op(acc, self.potential[v])
            self.potential[v] = acc
            self.parent[v] = r
        return r

    def dist(self, a: int, b: int) -> typing.Any:
        """aから見たbの重みを返す。未連結ならINF。ならしO(α(N))"""
        if self.root(a) != self.root(b):
            return self.INF
        return self._op(self._inv(self.potential[a]), self.potential[b])

    def unite(self, a: int, b: int, d: typing.Any) -> bool:
        """「aから見たbの重みがd」という関係を追加する。既に同じ集合ならFalseを返す。ならしO(α(N))"""
        ra, rb = self.root(a), self.root(b)
        if ra == rb:
            return False
        pa, pb = self.potential[a], self.potential[b]
        if self.parent[ra] <= self.parent[rb]:
            # raの集合の方が大きいので、rbをraに付ける。
            # 付けた後に op(pa, d) == op(potential[rb], pb) となるように決める
            self.parent[ra] += self.parent[rb]
            self.parent[rb] = ra
            self.potential[rb] = self._op(self._op(pa, d), self._inv(pb))
        else:
            # raをrbに付ける。付けた後に op(op(potential[ra], pa), d) == pb となるように決める
            self.parent[rb] += self.parent[ra]
            self.parent[ra] = rb
            self.potential[ra] = self._op(pb, self._inv(self._op(pa, d)))
        return True

    def size(self, a: int) -> int:
        """aの属する集合の要素数を返す。ならしO(α(N))"""
        return -self.parent[self.root(a)]

    def groups(self) -> typing.List[typing.List[int]]:
        """集合ごとの要素のリストを返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        return [g for g in G if g]

    def groups_index(self) -> typing.Tuple[typing.List[typing.List[int]], typing.List[int]]:
        """集合ごとの要素のリストと、根から集合の番号への対応を返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        cnt = 0
        GG = []
        I = [-1] * self.N
        for i in range(self.N):
            if G[i]:
                GG.append(G[i])
                I[i] = cnt
                cnt += 1
        return GG, I

    def group_size(self) -> typing.List[int]:
        """各集合の要素数のリストを返す。O(N α(N))"""
        G = [[] for _ in range(self.N)]
        for i in range(self.N):
            G[self.root(i)].append(i)
        return [len(g) for g in G if g]
