"""考察用の実験テンプレート（提出用ではない）

d:\\work で実行する（初回はこのファイルから d:\\work\\exp.py が作られる）:
    .\\exp.ps1          # exp.py を実行する（無ければテンプレートから作る）
    .\\exp.ps1 -New     # 別の問題を始めるとき。テンプレートから作り直す

流れ（くわしくは THINKING_GUIDE.md）:
    1. brute に全探索を書く（遅くてよい。正しさだけを考える）
    2. 小さい入力で答えを並べ、規則を探す（show / table）
    3. 規則から solve を書いたら、stress で全探索と比べる。反例が出たら 2 に戻る

下は例題「長さ N の順列を、隣り合う2つの入れ替えで昇順にする最小回数」で、
そのまま実行できる。問題に合わせて brute / solve / gen を書き換える。
入力を全部作る関数は、permutations の他に arrays / strings / trees / graphs がある。

https://github.com/yasyasyu/local-lib/blob/master/experiment_template.py
"""

from local_lib.experiment import bfs_states, permutations, show, stress, table


# ---- 1. 全探索 ----------------------------------------------------------------
def brute(p: tuple[int, ...]) -> int:
    """操作を全部試す。操作系の問題は bfs_states で状態を全部調べるのが基本"""

    def moves(s: tuple[int, ...]):
        for i in range(len(s) - 1):
            t = list(s)
            t[i], t[i + 1] = t[i + 1], t[i]
            yield tuple(t)

    return bfs_states(p, moves)[tuple(sorted(p))]


# ---- 2. 規則を探す ------------------------------------------------------------
for n in range(1, 5):
    print(f"--- N = {n}")
    show(brute, permutations(n))
# 答えが2つの値で決まるときは表にする（例: N と、答えが k になる順列の個数）
table(lambda n, k: sum(1 for p in permutations(n) if brute(p) == k), range(1, 6), range(0, 8))


# ---- 3. 規則から解法を書き、全探索と比べる -------------------------------------
def solve(p: tuple[int, ...]) -> int:
    """見つけた規則: 答えは転倒数（i < j かつ p[i] > p[j] の組の個数）"""
    n = len(p)
    return sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])


def gen(rng):
    n = rng.randint(1, 6)
    p = list(range(n))
    rng.shuffle(p)
    return tuple(p)


stress(solve, brute, gen)
