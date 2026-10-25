"""考察のための実験用の道具（ローカルで使う。提出用ではない）

小さい入力をすべて作って全探索し、答えを並べて規則を探す。見つけた解法は stress で全探索と比べる。
使い方の流れは experiment_template.py と THINKING_GUIDE.md を参照。

https://github.com/yasyasyu/local-lib/blob/master/experiment.py
"""

import itertools
import random
from collections import deque
from typing import Any, Callable, Hashable, Iterable, Iterator, TypeVar

S = TypeVar("S", bound=Hashable)


def arrays(n: int, lo: int, hi: int) -> Iterator[tuple[int, ...]]:
    """長さ n で、各要素が lo 以上 hi 以下の配列をすべて列挙する。O((hi - lo + 1)^n)

    使い方:
        list(arrays(2, 0, 1))   # [(0, 0), (0, 1), (1, 0), (1, 1)]

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    return itertools.product(range(lo, hi + 1), repeat=n)


def strings(n: int, alphabet: str = "ab") -> Iterator[str]:
    """長さ n で、alphabet の文字からなる文字列をすべて列挙する。O(|alphabet|^n)

    使い方:
        list(strings(2, "ab"))   # ["aa", "ab", "ba", "bb"]

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    return ("".join(t) for t in itertools.product(alphabet, repeat=n))


def permutations(n: int) -> Iterator[tuple[int, ...]]:
    """0, 1, ..., n - 1 の順列をすべて列挙する。O(n!)

    使い方:
        list(permutations(3))   # [(0, 1, 2), (0, 2, 1), ..., (2, 1, 0)]

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    return itertools.permutations(range(n))


def trees(n: int) -> Iterator[list[tuple[int, int]]]:
    """頂点 0, ..., n - 1 のラベル付き木を、辺のリストとしてすべて列挙する（n^(n-2) 個）。O(n^(n-2) * n^2)

    プリューファー列から木を復元して作る。n は 7 程度まで。

    使い方:
        len(list(trees(4)))   # 16
        for edges in trees(4):
            ...

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    if n == 1:
        yield []
        return
    for seq in itertools.product(range(n), repeat=n - 2):
        degree = [1] * n
        for x in seq:
            degree[x] += 1
        edges = []
        for x in seq:
            leaf = degree.index(1)  # 番号が最小の葉
            edges.append((leaf, x))
            degree[leaf] -= 1
            degree[x] -= 1
        u, v = [i for i in range(n) if degree[i] == 1]
        edges.append((u, v))
        yield edges


def graphs(n: int, connected: bool = False) -> Iterator[list[tuple[int, int]]]:
    """頂点 0, ..., n - 1 の単純無向グラフを、辺のリストとしてすべて列挙する。O(2^(n(n-1)/2) * n^2)

    connected=True なら連結なものだけ。n は 5（1024 個）〜 6（32768 個）程度まで。

    使い方:
        len(list(graphs(3)))                   # 8
        len(list(graphs(3, connected=True)))   # 4

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        if connected and not _is_connected(n, edges):
            continue
        yield edges


def _is_connected(n: int, edges: list[tuple[int, int]]) -> bool:
    """グラフが連結かを返す。O(n + m)"""
    if n == 0:
        return True
    G: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        G[u].append(v)
        G[v].append(u)
    seen = [False] * n
    seen[0] = True
    stack = [0]
    while stack:
        v = stack.pop()
        for u in G[v]:
            if not seen[u]:
                seen[u] = True
                stack.append(u)
    return all(seen)


def bfs_states(start: S, moves: Callable[[S], Iterable[S]]) -> dict[S, int]:
    """状態 start から、操作 moves で行ける状態すべてと、そこまでの最小の操作回数を返す。O(状態数 × 遷移数)

    「この操作を繰り返して目標にできるか」「最小何回か」を全探索するときに使う。
    状態はタプルや文字列など、ハッシュできるもので表す（リストは不可）。

    使い方:
        # 隣り合う2つを入れ替える操作
        def moves(p):
            for i in range(len(p) - 1):
                q = list(p)
                q[i], q[i + 1] = q[i + 1], q[i]
                yield tuple(q)

        dist = bfs_states((2, 0, 1), moves)
        dist[(0, 1, 2)]      # 2（昇順にする最小回数）
        (1, 0, 2) in dist    # True（たどり着けるか）

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        d = dist[s] + 1
        for t in moves(s):
            if t not in dist:
                dist[t] = d
                q.append(t)
    return dist


def show(f: Callable[[Any], Any], inputs: Iterable[Any]) -> None:
    """各入力について「入力 -> f(入力)」を1行ずつ表示する。O(入力の個数 × f)

    使い方:
        show(brute, permutations(3))
        # (0, 1, 2) -> 0
        # (0, 2, 1) -> 1
        # ...

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    for x in inputs:
        print(f"{x} -> {f(x)}")


def table(f: Callable[[int, int], Any], rows: Iterable[int], cols: Iterable[int]) -> None:
    """f(i, j) を、行 i・列 j の表にして表示する。O(行数 × 列数 × f)

    答えが2つの値（N と K など）で決まるときに、規則を探すのに使う。

    使い方:
        table(lambda n, k: n * k, range(1, 4), range(0, 3))
        #   | 0 1 2
        # ---------
        # 1 | 0 1 2
        # 2 | 0 2 4
        # 3 | 0 3 6

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    rows = list(rows)
    cols = list(cols)
    cells = [[str(f(i, j)) for j in cols] for i in rows]
    w = max([len(str(j)) for j in cols] + [len(c) for row in cells for c in row] + [1])
    wr = max([len(str(i)) for i in rows] + [1])
    print(" " * wr + " |" + "".join(f" {j:>{w}}" for j in cols))
    print("-" * (wr + 2 + (w + 1) * len(cols)))
    for i, row in zip(rows, cells):
        print(f"{i:>{wr}} |" + "".join(f" {c:>{w}}" for c in row))


def stress(
    solve: Callable[[Any], Any],
    brute: Callable[[Any], Any],
    gen: Callable[[random.Random], Any],
    trials: int = 1000,
    seed: int = 0,
) -> Any | None:
    """gen で作ったランダムな入力で solve と brute を比べ、最初に答えが違った入力を返す（無ければ None）。

    計算量: O(trials × (solve + brute))
    gen(rng) は乱数生成器 rng を受け取り、入力を1つ返す（引数が複数なら、タプルにまとめる）。
    答えが違ったら、その入力と両方の答えを表示する。反例は小さい方が調べやすいので、
    gen では小さい入力（N <= 6 程度）を作るとよい。

    使い方:
        def gen(rng):
            n = rng.randint(1, 6)
            return tuple(rng.randint(0, 3) for _ in range(n))

        stress(solve, brute, gen)
        # 反例: (2, 0, 1)
        #   solve: 1
        #   brute: 2

    https://github.com/yasyasyu/local-lib/blob/master/experiment.py
    """
    rng = random.Random(seed)
    for _ in range(trials):
        x = gen(rng)
        a = solve(x)
        b = brute(x)
        if a != b:
            print(f"反例: {x!r}")
            print(f"  solve: {a!r}")
            print(f"  brute: {b!r}")
            return x
    print(f"{trials} 件すべて一致")
    return None
