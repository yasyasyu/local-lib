# Local Library

競技プログラミング用のローカルライブラリとツール群です。

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
