# SegTree / LazySegTree の使い方（ac-library-python）

## SegTree（1点更新・区間集約）

`SegTree(op, e, v)` に渡す要素:

- **`v`**: 初期配列（`list`）。列の各要素の初期値。要素数だけを渡したい場合は`int`でもよく、その場合は全要素が`e`で初期化される。
- **`op(x, y)`**: 2引数関数。値`x`と`y`を1つに結合して返す。列を2つに分けたときの「左側の集約値`x`」と「右側の集約値`y`」を受け取り、「その2つを繋げた列全体の集約値」を返すイメージ。結合律`op(op(a,b),c) == op(a,op(b,c))`を満たす必要がある（可換である必要はなく、常に`x`が左側・`y`が右側として呼ばれることが保証される）。
- **`e`**: `op`の単位元。`op(e, x) == op(x, e) == x`を満たす値。空区間（`prod(l, l)`）のクエリ結果になるほか、内部で配列長を2冪に切り上げる際の埋め草としても使われる。

```python
from atcoder.segtree import SegTree

INF = 10**9

# 区間和（RSQ）
seg = SegTree(op=lambda x, y: x + y, e=0, v=a)

# 区間min（RmQ）
seg = SegTree(op=min, e=INF, v=a)

# 区間max（RMQ）
seg = SegTree(op=max, e=-INF, v=a)

# 区間gcd
import math
seg = SegTree(op=math.gcd, e=0, v=a)
```
`seg.set(p, x)`で1点更新、`seg.get(p)`で1点取得、`seg.prod(l, r)`で区間[l,r)の集約値を取得する。

**`max_right(l, g)` / `min_left(r, g)`（セグ木上の二分探索）**

集約値に対する単調な条件`g`を満たす境界を、O(log N)で二分探索する。`g(e)`が`True`であることが前提（内部で`assert`される）。

- `max_right(l, g)`: `g(prod(l, r))`が`True`になる最大の`r`（`l <= r <= n`）を返す。`g`は「`r`を増やすと`prod(l, r)`が単調に条件を満たしにくくなる」性質（一度`False`になったら、それより右では二度と`True`に戻らない）を満たす必要がある。
- `min_left(r, g)`: `g(prod(l, r))`が`True`になる最小の`l`（`0 <= l <= r`）を返す。同様に「`l`を減らす（区間を左に広げる）と単調に条件を満たしにくくなる」性質が必要。

```python
# 非負整数列で、区間和がK以下になる最大の右端を求める（尺取り法のセグ木版）
seg = SegTree(op=lambda x, y: x + y, e=0, v=a)  # aは非負整数の列
r = seg.max_right(l, lambda s: s <= K)  # sum(a[l:r]) <= K を満たす最大のr
l2 = seg.min_left(r, lambda s: s <= K)  # sum(a[l2:r]) <= K を満たす最小のl2
```
`LazySegTree`にも同名・同シグネチャのメソッドがあり、集約値（S型）に対して同じように使える。

---

## LazySegTree（区間更新・区間集約）

`LazySegTree(op, e, mapping, composition, id_, v)` に渡す要素:

- **`v`**, **`op`**, **`e`**: 上のSegTreeと同じ（値`S`同士の集約）。`v`は初期配列（または要素数の`int`）、`op(x, y)`は値同士の結合、`e`は`op`の単位元。
- **`mapping(f, x)`**: 2引数関数。作用`f`を値`x`に適用した結果（適用後の値）を返す。**第1引数が作用`f`、第2引数が値`x`**という順序に注意（逆にすると動かない）。
- **`composition(f, g)`**: 2引数関数。「先に作用`g`を適用し、その後に作用`f`を適用する」のと同じ効果を持つ、合成後の単一の作用を返す。`mapping(composition(f, g), x) == mapping(f, mapping(g, x))`を満たす必要がある（`g`が先に効いていた古い作用、`f`が後から追加された新しい作用）。
- **`id_`**: 作用の恒等写像（`F`の単位元）。`mapping(id_, x) == x`を満たす値。「まだ何も更新が保留されていない」状態を表すのにも使われる。

上記6パターンのように、値の型（S型）と作用の型（F型）は別々に設計してよい（例: Sは`int`、Fは`Optional[int]`など）。

参考: [AtCoder Library Lazy SegTree チートシート (betrue12)](https://betrue12.hateblo.jp/entry/2020/09/23/005940)

```python
from atcoder.lazysegtree import LazySegTree

INF = 10**9
```

**1. RAQ + RmQ（区間加算・区間最小値取得）**

- `S=int, F=int`
- `op=min, e=INF`
- `mapping(f,x)=f+x`
- `composition(f,g)=f+g`
- `id_=0`

```python
seg = LazySegTree(
    op=min, e=INF,
    mapping=lambda f, x: f + x,
    composition=lambda f, g: f + g,
    id_=0,
    v=a,
)
```

**2. RAQ + RMQ（区間加算・区間最大値取得）**

- `S=int, F=int`
- `op=max, e=-INF`
- `mapping(f,x)=f+x`
- `composition(f,g)=f+g`
- `id_=0`

```python
seg = LazySegTree(
    op=max, e=-INF,
    mapping=lambda f, x: f + x,
    composition=lambda f, g: f + g,
    id_=0,
    v=a,
)
```

**3. RAQ + RSQ（区間加算・区間和取得）**

「加算量 × 区間長」を足す必要があるため、S=(合計値, 要素数)のペアで持つ。

- `S=(int, int), F=int`
- `op=要素ごとの和, e=(0, 0)`
- `mapping(f,(s,l))=(s+f*l, l)`
- `composition(f,g)=f+g`
- `id_=0`


```python
seg = LazySegTree(
    op=lambda x, y: (x[0] + y[0], x[1] + y[1]), e=(0, 0),
    mapping=lambda f, x: (x[0] + f * x[1], x[1]),
    composition=lambda f, g: f + g,
    id_=0,
    v=[(x, 1) for x in a],
)
# 合計値は seg.prod(l, r)[0] で取り出す
```

**4. RUQ + RmQ（区間変更・区間最小値取得）**

- `S=int, F=Optional[int]`
- `op=min, e=INF`
- `mapping(f,x)=x if f is None else f`
- `composition(f,g)=g if f is None else f`
- `id_=None`


```python
seg = LazySegTree(
    op=min, e=INF,
    mapping=lambda f, x: x if f is None else f,
    composition=lambda f, g: g if f is None else f,
    id_=None,
    v=a,
)
```

**5. RUQ + RMQ（区間変更・区間最大値取得）**

- `S=int, F=Optional[int]`
- `op=max, e=-INF`
- `mapping(f,x)=x if f is None else f`
- `composition(f,g)=g if f is None else f`
- `id_=None`

```python
seg = LazySegTree(
    op=max, e=-INF,
    mapping=lambda f, x: x if f is None else f,
    composition=lambda f, g: g if f is None else f,
    id_=None,
    v=a,
)
```

**6. RUQ + RSQ（区間変更・区間和取得）**

- `S=(int, int), F=Optional[int]`
- `op=要素ごとの和, e=(0, 0)`
- `mapping(f,(s,l))=(s,l) if f is None else (f*l, l)`
- `composition(f,g)=g if f is None else f`
- `id_=None`


```python
seg = LazySegTree(
    op=lambda x, y: (x[0] + y[0], x[1] + y[1]), e=(0, 0),
    mapping=lambda f, x: x if f is None else (f * x[1], x[1]),
    composition=lambda f, g: g if f is None else f,
    id_=None,
    v=[(x, 1) for x in a],
)
```


`seg.apply(l, r, f)`で区間[l,r)に作用fを適用、`seg.apply(p, f=f)`で1点だけに適用、
`seg.get(p)`で1点取得、`seg.prod(l, r)`で区間集約値を取得する。

**ハマりどころ**
- RUQの番人（`id_=None`）は、実際のデータ値としてNoneを使わないことが前提。Noneが有効な値になり得る場合は、`8*10**18`のような専用の番兵値にする。
- RSQ系は`prod(l, r)`の戻り値が`(合計, 区間長)`のタプルなので、合計だけ使うときは`[0]`を忘れずに取り出す。
- `id_`（Fの単位元）を間違えると、`get`や`prod`の内部で無関係な葉（配列外の埋め草）に`mapping`が適用されたときに例外や誤った値になることがある。`mapping(id_, e)`が必ず安全に評価できる組み合わせにする。
- **RAQ+RmQ/RMQの`INF`は有限の値（例: `10**9`）だと危険な場合がある**。配列外の埋め草(`e`)にも`push`のたびに実際の加算値が積み重なっていくため、操作回数が多く加算量の絶対値も大きい問題では`INF`が実際のデータ範囲まで縮む（あるいは`-INF`が伸びる）恐れがある。`float("inf")`を使うか、想定される加算量の総和より十分大きい値（`4*10**18`など）を使うほうが安全（RUQ系はNoneが番人なので、この問題は起きない）。

## モノイド設計の考え方（発展）

参考: [区間クエリのためのモノイド設計 (AtCoder公式)](https://info.atcoder.jp/entry/algorithm_lectures/range_query_monoid_design)

核心の原則: 列Xに対して知りたい情報を`f(X)`として定義し、`op(f(X), f(Y)) = f(X++Y)`
（Xの後にYを繋げた列の情報）を満たすように`op`を設計する。単位元`e`は「空列の情報」`f([])`。
この条件（準同型であること）さえ満たせば、結合則と単位元の性質は自動的に成り立つ。

**複数の情報をまとめて持つ**: 1つの値だけでは表現できない情報は、タプルにまとめて
`op`の中でそれぞれ計算すればよい。

```python
INF = 10**9

# 区間最小値とその個数
def op(x, y):
    if x[0] == y[0]:
        return (x[0], x[1] + y[1])
    return x if x[0] < y[0] else y

seg = SegTree(op=op, e=(INF, 0), v=[(x, 1) for x in a])

# 区間の総和・最小値・最大値を同時に管理
def op(x, y):
    return (x[0] + y[0], min(x[1], y[1]), max(x[2], y[2]))

seg = SegTree(op=op, e=(0, INF, -INF), v=[(x, x, x) for x in a])
```

**情報を段階的に追加する**: 「今持っている情報だけでは`op`が組めない」ときは、結合に必要な情報を追加していく。たとえば「区間の第2最小値」は最小値だけでは求まらないので、最小値も一緒に持つ（同様に「区間内の平均値」は、平均そのものではなく「合計と個数」を持てば結合できる——これは上のRSQの`(合計, 要素数)`パターンと同じ発想）。

```python
# 区間の最小値・第2最小値（多重集合として）
def op(x, y):
    lo, hi = sorted([x[0], x[1], y[0], y[1]])[:2]
    return (lo, hi)

seg = SegTree(op=op, e=(INF, INF), v=[(x, INF) for x in a])
```

**単位元の選び方**: `e`（空列の情報）は`INF`や`0`のような値で自然に表現できることが多いが、状態が複雑で「都合の良い番人」を作りにくい場合は、`is_empty`フラグを持たせて空列を明示的に区別する方法も有効。

**LazySegTreeの「作用」もモノイド**: 区間更新側（F型）も同じ発想で設計できる。列の各要素を関数とみなし、列全体を関数の合成と考えるのが基本形（`composition`は関数合成、`mapping`は関数適用に対応する）。代表例がアフィン変換`f(x) = a*x + b`で、これを使うと**区間加算(RAQ)と区間代入(RUQ)を統一的に**扱える（RAQは`a=1`、RUQは`a=0`の特殊ケースとして表現できる。Library Checkerの「Range Affine Range Sum」として知られる問題そのもの）。

```python
MOD = 998244353

def op(x, y):
    return ((x[0] + y[0]) % MOD, x[1] + y[1])

def mapping(f, x):
    a, b = f
    s, l = x
    return ((a * s + b * l) % MOD, l)

def composition(f, g):
    # gを先に適用してからfを適用する
    a1, b1 = f
    a2, b2 = g
    return ((a1 * a2) % MOD, (a1 * b2 + b1) % MOD)

seg = LazySegTree(
    op=op, e=(0, 0),
    mapping=mapping, composition=composition, id_=(1, 0),  # 恒等変換 x -> 1*x+0
    v=[(x, 1) for x in a],
)
seg.apply(l, r, (1, c))  # 区間加算（RAQ相当）: x -> x + c
seg.apply(l, r, (0, c))  # 区間代入（RUQ相当）: x -> c
```

いずれも乱数ブルートフォースで動作確認済み。

## さらに複雑な例（元記事の具体例、続き）

AtCoder公式記事で挙げられている残りの具体例。いずれも乱数ブルートフォースで動作確認済み。

**数字列が表す整数**（部分文字列が表す整数値をmodで求める）
- S=(value, pow10) / e=(0, 1) / 葉（数字d）=(d, 10)
```python
MOD = 998244353

def op(x, y):
    return ((x[0] * y[1] + y[0]) % MOD, (x[1] * y[1]) % MOD)

seg = SegTree(op=op, e=(0, 1), v=[(d, 10) for d in digits])
# digits[l:r] が表す整数値(mod MOD) は seg.prod(l, r)[0]
```

**「ABC」部分列の個数**（文字列中でi<j<kかつs[i]=A, s[j]=B, s[k]=Cとなる三つ組の個数）
- S=(ABC, AB, BC, A, B, C) の6値 / e=すべて0 / 文字cの葉は該当する1箇所だけ1、他0
- 境界をまたぐ「左のAB×右のC」「左のA×右のBC」のような組み合わせを数え上げる
```python
def leaf(c):
    return {"A": (0,0,0,1,0,0), "B": (0,0,0,0,1,0), "C": (0,0,0,0,0,1)}.get(c, (0,0,0,0,0,0))

def op(x, y):
    ABC = x[0] + x[1]*y[5] + x[3]*y[2] + y[0]
    AB  = x[1] + x[3]*y[4] + y[1]
    BC  = x[2] + x[4]*y[5] + y[2]
    A, B, C = x[3]+y[3], x[4]+y[4], x[5]+y[5]
    return (ABC, AB, BC, A, B, C)

seg = SegTree(op=op, e=(0,0,0,0,0,0), v=[leaf(c) for c in s])
```

**最大部分配列和**（Kadane法のセグ木版。空でない部分列が対象）
- S=(ans, prefix, suffix, full) / e=(-INF, -INF, -INF, 0) / 葉(v)=(v, v, v, v)
```python
def op(x, y):
    ans = max(x[0], y[0], x[2] + y[1])
    prefix = max(x[1], x[3] + y[1])
    suffix = max(x[2] + y[3], y[2])
    full = x[3] + y[3]
    return (ans, prefix, suffix, full)

seg = SegTree(op=op, e=(-INF, -INF, -INF, 0), v=[(v, v, v, v) for v in a])
```

**関数 x ↦ min(x+a, b) の合成**（アフィン変換をさらに一般化。区間chmin+区間加算を統一的に扱える）
- S=(a, b) / e=(0, INF)
- op(x,y) = (x.a+y.a, min(x.b+y.a, y.b))　※列の並び通り、xを先に適用してからyを適用する合成
```python
def op(x, y):
    return (x[0] + y[0], min(x[1] + y[0], y[1]))

seg = SegTree(op=op, e=(0, INF), v=fs)  # fs[i] = (a_i, b_i)
# seg.prod(l, r) は fs[l], fs[l+1], ..., fs[r-1] の順に適用した関数 (a, b) を表す
# 実際の値に適用するには min(x + a, b) を計算する
```

**「ABC」部分列の最小コスト**（各文字に重みがあり、A→B→Cの順で選んだときのコスト和の最小値を求める）
- 上のABC個数と同じ6フィールドだが、min-plus半環（通常の`+`と`min`を入れ替えたもの）で計算する
- e=すべて`INF`（0個の要素では何も達成できないことを表す）

> 注意: AtCoder公式記事の式をそのまま試したところ、単一文字フィールド(A/B/C)の結合だけブルートフォースと一致しなかった（`x.A + y.A`のような単純な和ではなく、`min(x.A, y.A)`が正しい——「複数のうちコストが最小の1つを選ぶ」ので、他のフィールドと同じくminで合成する必要がある）。以下は実際に動作確認済みの式。

```python
def leaf(c, cost):
    base = [INF, INF, INF, INF, INF, INF]
    idx = {"A": 3, "B": 4, "C": 5}.get(c)
    if idx is not None:
        base[idx] = cost
    return tuple(base)

def op(x, y):
    ABC = min(x[0], x[1] + y[5], x[3] + y[2], y[0])
    AB  = min(x[1], x[3] + y[4], y[1])
    BC  = min(x[2], x[4] + y[5], y[2])
    A, B, C = min(x[3], y[3]), min(x[4], y[4]), min(x[5], y[5])
    return (ABC, AB, BC, A, B, C)

seg = SegTree(op=op, e=(INF,)*6, v=[leaf(c, cost) for c, cost in zip(chars, costs)])
```

**単純なモノイド設計だけでは解けない例（元記事より）**

「順列の転倒数」と「区間内の相異なる値の個数」の2つは、単純な区間モノイドの結合だけでは求まらない。元記事でも「問題の言い換え」や「処理順序の工夫」が本質だと説明されている。

- 転倒数: 各要素について「自分より値が大きく、かつ自分より前にある要素の個数」を数える。値をインデックスとしたBIT/SegTreeに左から順に1点更新しながら区間和を取る、というオフライン処理が必要。
- 区間内の相異なる値の個数: クエリを右端`R`の昇順にソートし、値ごとに「直前に出現した位置」のフラグだけを立てておき、`R`を進めるたびに古い出現位置のフラグを消して新しい出現位置のフラグを立てる、という工夫（オフラインBIT）が必要。

どちらも`ac-library-python`の`atcoder.fenwicktree.FenwickTree`と組み合わせて実装できる（単純な`op`/`e`の定義だけでは完結しない）。

## 区間更新・1点取得だけでよい場合（双対セグ木）

区間の集約（`prod`）が不要なら、上のLazySegTreeの例から`op`と`e`をダミー
（`op=lambda a, b: a`, `e`は`mapping(id_, e)`がエラーにならない適当な値）に差し替えれば、
「区間更新・1点取得」（代入のような非可換な更新にも対応できる）として使える。
`seg.get(p)`だけを使い、`prod`/`all_prod`/`max_right`/`min_left`は呼ばない。

加算・min・max・xorのように**適用順序を入れ替えても結果が変わらない（可換）**演算しか
使わないなら、伝播(push)自体が不要になるため、LazySegTreeを使わずに自前の非再帰セグ木
（区間更新はO(log N)個のノードへの書き込み、1点取得は葉から根への合成のみ）で組む方が
定数倍が軽い。ただし代入のような非可換な更新には使えない（後から適用した方が必ず勝つとは
限らないため、木の形と適用順序が食い違うケースで壊れる）。
