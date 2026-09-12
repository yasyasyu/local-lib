# Local Library

競技プログラミング用のローカルライブラリとツール群です。

## ライブラリ一覧

ファイルはフォルダを分けず全て直下に置いている（提出用に`expander`で展開する際のimportを短く保つため）。
その代わり、ここでカテゴリ別に索引を作っておく。

### Union-Find系

| ファイル | 内容 |
| --- | --- |
| `union_find.py` | Union-Find（素集合データ構造） |
| `potential_union_find.py` | 重み付きUnion-Find |
| `rollback_union_find.py` | rollback（undo）可能なUnion-Find |

### データ構造（集合・ヒープなど）

| ファイル | 内容 |
| --- | --- |
| `sorted_set.py` | 昇順ソート済み集合（重複なし） |
| `sorted_multi_set.py` | 昇順ソート済み多重集合（重複あり） |
| `interval_set.py` | 区間の集合を管理するデータ構造（`sorted_multi_set.py`に依存） |
| `bucket_list.py` | 平方分割による可変長リスト |
| `deletable_heap.py` | 削除可能なヒープ |
| `persistent_stack.py` | 永続スタック |
| `li_chao_tree.py` | Li Chao Tree（直線群の最小値クエリ） |
| `trie.py` | 文字列Trie木、およびXORクエリ用のBinaryTrie |
| `fenwick_tree_2d.py` | 2次元Fenwick Tree（点更新・矩形和取得。列方向に`ac-library-python`の`FenwickTree`を使う） |
| `segment_tree_2d.py` | 2次元セグメント木（点更新・矩形集約、任意の可換モノイド用。列方向に`ac-library-python`の`SegTree`を使う） |

セグメント木・遅延セグメント木・Fenwick Tree（1次元）など`ac-library-python`にある機能は実装せず、
[USAGE_SegTree.md](USAGE_SegTree.md)に使い方一覧をまとめている。`fenwick_tree_2d.py`と
`segment_tree_2d.py`は、列方向の1次元構造として`ac-library-python`の`FenwickTree`/`SegTree`を
そのまま利用しているため、この2ファイルだけ`ac-library-python`が必要
（他のファイルは標準ライブラリのみで動作する）。

### グラフ・木

| ファイル | 内容 |
| --- | --- |
| `scc.py` | 強連結成分分解（Kosaraju法） |
| `topological_sort.py` | トポロジカルソート |
| `kruskal.py` | クラスカル法による最小全域木（`union_find.py`に依存） |
| `dijkstra.py` | 単一始点最短路（ダイクストラ法） |
| `bellman_ford.py` | 単一始点最短路（ベルマンフォード法、負閉路検出対応） |
| `warshall_floyd.py` | 全点対最短路（ワーシャルフロイド法） |
| `euler_tour.py` | オイラーツアー（深さ・部分木の管理） |
| `doubling.py` | ダブリング（写像の高速反復適用） |
| `lca.py` | 最小共通祖先（LCA、`doubling.py`に依存） |

### 数学

| ファイル | 内容 |
| --- | --- |
| `_math.py` | 約数列挙・素数篩・素因数分解・区間篩 |
| `isqrt.py` | 整数の平方根（floor） |
| `combinatorics.py` | mod付き組合せ論（階乗・逆元テーブルによるnCr等） |
| `matrix_pow.py` | 行列累乗（繰り返し二乗法） |

### 文字列

| ファイル | 内容 |
| --- | --- |
| `rolling_hash.py` | ローリングハッシュ |
| `lcs.py` | 最長共通部分列（LCS） |

### 幾何

| ファイル | 内容 |
| --- | --- |
| `geometry.py` | 凸包・線分交差判定・点と多角形の内外判定 |

### クエリ処理テクニック

| ファイル | 内容 |
| --- | --- |
| `mo.py` | Moのアルゴリズム（オフライン区間クエリの高速化） |

### 配列・グリッド操作

| ファイル | 内容 |
| --- | --- |
| `cumulative_sum_2d.py` | 2次元累積和 |
| `compress.py` | 座標圧縮 |
| `rle.py` | ランレングス圧縮 |
| `rotate90.py` | グリッドの90度回転・転置 |
| `grid_trim.py` | グリッドの余白トリム |
| `bit_partial_set.py` | ビットマスクの部分集合列挙 |

### テンプレート／開発ツール

| ファイル | 内容 |
| --- | --- |
| `deciding_binary_search.py` | 二分探索テンプレート（`is_ok`は問題ごとに書き換える） |
| `add_treeview.py` | セグ木風クラスに`__str__`でツリー表示を追加するデコレータ |
| `_parser.py` | 四則演算パーサー |

各モジュールに対応するテストは `tests/test_*.py` にあります。以下でまとめて実行できます。

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## expander（提出用インポート展開ツール）

Pythonファイル内のローカルライブラリのインポート文を展開して、1つのファイルにまとめるツールです。競技プログラミングの提出時に便利です。

**別リポジトリ [yasyasyu/py-import-expander](https://github.com/yasyasyu/py-import-expander) として切り出し、このリポジトリには`expander`ディレクトリにgit submoduleとして組み込んでいます。** 使い方・プルーニング（使っている名前だけを展開する機能）・クラス構造・制限事項などの詳細はそちらのREADMEを参照してください。

### セットアップ

このリポジトリをcloneした直後はsubmoduleの中身が空なので、以下のどちらかで取得する。

```bash
# clone時にsubmoduleも一緒に取得する場合
git clone --recurse-submodules https://github.com/yasyasyu/local-lib.git

# すでにcloneしてある場合
git submodule update --init
```

### 使い方

```bash
python expander/expander.py main.py local_lib > output.py
```

### submoduleの更新

`py-import-expander`側で更新があった場合、このリポジトリ側のsubmoduleを最新に追従させるには:

```bash
git submodule update --remote expander
git add expander
git commit -m "expanderを最新化"
```
