# Local Library

競技プログラミング用のローカルライブラリとツール群です。

## ライブラリ一覧

ファイルはフォルダを分けず全て直下に置いている（提出用に`expander.py`で展開する際のimportを短く保つため）。
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

セグメント木・遅延セグメント木・Fenwick Treeなど`ac-library-python`にある機能は実装せず、
[USAGE_SegTree.md](USAGE_SegTree.md)に使い方一覧をまとめている。

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
| `expander.py` | 提出用にローカルライブラリのインポートを展開するツール（詳細は下記） |

各モジュールに対応するテストは `tests/test_*.py` にあります。以下でまとめて実行できます。

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## expander.py

Pythonファイル内のローカルライブラリのインポート文を展開して、1つのファイルにまとめるツールです。競技プログラミングの提出時に便利です。

### 使い方

#### 基本的な使い方

```bash
python expander.py <入力ファイル> > <出力ファイル>
```

展開対象フォルダを指定する場合:
```bash
python expander.py <入力ファイル> <展開対象フォルダ> > <出力ファイル>
```

- **デフォルト動作**: 標準出力に展開結果を出力します
- **展開対象フォルダ**: 省略した場合、`expander.py`があるディレクトリを使用します

#### 例

```bash
# 基本的な使い方（local_libフォルダから展開）
python expander.py main.py > output.py

# 展開対象フォルダを明示的に指定
python expander.py main.py local_lib > output.py

# 標準出力で確認
python expander.py main.py
```

#### 実行例

入力ファイル `main.py`:
```python
from local_lib.interval_set import IntervalSet

N, Q = map(int, input().split())
interval_set = IntervalSet()
```

実行:
```bash
python expander.py main.py > output.py
```

出力 `output.py`:
```python
# from local_lib.interval_set import IntervalSet
################ local_lib/interval_set start ################
# from .sorted_multi_set import SortedMultiset
################ local_lib/sorted_multi_set start ################
# (sorted_multi_setの内容が展開される)
################ local_lib/sorted_multi_set end ################

# (interval_setの内容が展開される)
################ local_lib/interval_set end ################

N, Q = map(int, input().split())
interval_set = IntervalSet()
```

### サポートされるインポート形式

- **相対インポート**: `from .module import Class`
- **絶対インポート（ドット区切り）**: `from local_lib.module import Class`

### クラス構造

#### コアクラス

##### `ParsedImport` (dataclass)
パースされたインポート文の情報を保持します。
- `module_file_path`: モジュールファイルの絶対パス
- `module`: モジュール名（スラッシュ区切り）

##### `ImportParser`
インポート文をパースする責務を持ちます。

**主要メソッド:**
- `calculate_indent_level(line)`: 行のインデントレベルを計算
- `should_expand(line)`: 展開対象かどうかを判定
- `parse_relative_import(line)`: 相対インポート（`from .`）をパース
- `parse_absolute_import(line)`: 絶対インポート（`from folder.module`）をパース
- `parse(line)`: インポート文を統合的にパース

##### `ModuleExpander`
モジュールを展開する責務を持ちます。

**主要メソッド:**
- `expand_line(line, indent)`: 1行のインポート文を展開
- `expand_file(file_path)`: ソースファイル全体を処理
- **状態管理**: `expanded_modules`で展開済みモジュールを追跡（重複防止）

**特徴:**
- 同じモジュールは1度だけ展開されます
- 展開状況は標準エラー出力に表示されます（`Expand module` / `Skip module`）

##### `ExpanderConfig`
設定を管理します。

**主要メソッド:**
- `from_command_line()`: コマンドライン引数から設定を作成
- プロパティ: `file_path`, `expand_path`, `expand_folder`

**動作:**
- `expand_path`を省略した場合、`expander.py`と同じディレクトリを使用

##### `ExpanderApplication`
アプリケーション全体を統括します。

**主要メソッド:**
- `run()`: アプリケーションを実行し、結果を標準出力に出力

### 設計の利点

1. **単一責任の原則**: 各クラスが明確な責務を持つ
2. **テスト容易性**: 各クラスを独立してテスト可能
3. **状態管理**: `expanded_modules`がインスタンス変数として適切に管理
4. **拡張性**: 新しいインポート形式の追加が容易
5. **可読性**: クラス名とメソッド名から意図が明確

### 処理フロー

```
ExpanderApplication
  ↓
ExpanderConfig（設定管理）
  ↓
ModuleExpander（展開処理）
  ├─ ImportParser（インポート解析）
  │   ├─ should_expand（判定）
  │   └─ parse（パース）
  └─ expanded_modules（重複管理）
```

### テスト

テストコードは `tests/test_expander.py` にあります。

```bash
cd tests
python test_expander.py
```

**テストクラス:**
- `TestImportParser`: パーサーの各メソッドをテスト
- `TestExpanderConfig`: 設定解析をテスト
- `TestModuleExpander`: 展開処理の統合テスト

### 制限事項

- `import module` 形式（相対/絶対どちらでも）は未サポート
- `from module import Class` 形式のみサポート（ドット区切り必須）
- Python 3.10以上が必要（型ヒント `|` を使用）

### トラブルシューティング

**Q: `FileNotFoundError: Module file not found` が出る**  
A: モジュールファイルのパスが正しいか確認してください。相対インポートの場合、カレントディレクトリに注意が必要です。

**Q: モジュールが展開されない**  
A: 標準エラー出力で `Skip module` と表示される場合、すでに展開済みです。`Expand module` と表示されない場合、インポート形式が未サポートの可能性があります。
