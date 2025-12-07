import os
import sys
from dataclasses import dataclass
from typing import Optional

SPACE = " "
INDENT_SIZE = 4
INDENT = SPACE * INDENT_SIZE
SEPARATOR_LENGTH = INDENT_SIZE * INDENT_SIZE


@dataclass
class ParsedImport:
    """パースされたインポート文の情報"""

    module_file_path: str
    module: str


class ImportParser:
    """インポート文をパースするクラス"""

    def __init__(self, expand_folder: str):
        self.expand_folder = expand_folder

    @staticmethod
    def calculate_indent_level(line: str) -> int:
        """行のインデントレベルを計算する"""
        return (len(line) - len(line.lstrip())) // len(INDENT)

    def should_expand(self, line: str) -> bool:
        """この行を展開すべきかどうかを判定する"""
        stripped = line.lstrip()
        return (
            stripped.startswith(f"from {self.expand_folder}")
            or stripped.startswith("from .")
            or stripped.startswith(f"import {self.expand_folder}")
        )

    def parse_relative_import(self, line: str) -> ParsedImport:
        """相対インポート (from .) をパースする"""
        parts = line.split("import")
        module = parts[0].replace("from .", "").strip()

        if "." in module:
            # ネストされたモジュールの場合: from .folder.filename import classname
            module_file_path = os.path.abspath(
                f"./{self.expand_folder}/{'/'.join(module.split('.'))}.py"
            )
            module = f"{self.expand_folder}/{'/'.join(module.split('.'))}"
        else:
            # シンプルなモジュール: from .folder import filename
            module_file_path = os.path.abspath(f"./{self.expand_folder}/{module}.py")
            module = f"{self.expand_folder}/{module}"

        return ParsedImport(module_file_path, module)

    @staticmethod
    def parse_absolute_import(line: str) -> ParsedImport:
        """絶対インポート (from folder) をパースする"""
        parts = line.split("import")
        module = parts[0].replace("from ", "").strip()

        if "." not in module:
            raise ValueError(
                "from folder.filename import classname の形式のみサポートされています。"
            )

        # ネストされたモジュールの場合
        module_file_path = os.path.abspath(f"./{'/'.join(module.split('.'))}.py")
        module = "/".join(module.split("."))

        return ParsedImport(module_file_path, module)

    def parse(self, line: str) -> ParsedImport:
        """インポート文をパースしてモジュール情報を返す"""
        stripped_line = line.lstrip()

        if stripped_line.startswith("from ."):
            return self.parse_relative_import(line)
        elif stripped_line.startswith("from "):
            return self.parse_absolute_import(line)
        elif stripped_line.startswith("import "):
            raise ValueError(
                "from folder.filename import classname の形式のみサポートされています。"
            )
        else:
            raise ValueError(f"サポートされていないインポート文: {line}")


class ModuleExpander:
    """モジュールを展開するクラス"""

    def __init__(self, expand_folder: str):
        self.expand_folder = expand_folder
        self.parser = ImportParser(expand_folder)
        self.expanded_modules: set[str] = set()

    def expand_line(self, line: str, current_space_indent: int) -> Optional[str]:
        """インポート行を展開する。展開対象でない場合はNoneを返す"""
        if not self.parser.should_expand(line):
            return None

        expand_results = []
        space_indent = self.parser.calculate_indent_level(line)

        # コメントとして元のインポート文を残す
        expand_results.append(
            f"{INDENT * (space_indent + current_space_indent)}# {line.lstrip()}"
        )

        # インポート文をパースしてモジュール情報を取得
        parsed = self.parser.parse(line)

        # 重複チェック
        if parsed.module in self.expanded_modules:
            print(f"Skip module\t[{parsed.module}]", file=sys.stderr)
            return "\n".join(expand_results)

        self.expanded_modules.add(parsed.module)
        print(f"Expand module\t[{parsed.module}]", file=sys.stderr)

        # モジュールの内容を展開
        expand_results.append(
            self._expand_module_file(
                parsed.module_file_path,
                parsed.module,
                space_indent + current_space_indent,
            )
        )
        return "\n".join(expand_results)

    def _expand_module_file(
        self, module_file_path: str, module: str, space_indent: int
    ) -> str:
        """モジュールファイルの内容を展開する"""
        expand_results = []
        expand_results.append(
            f"{INDENT * space_indent}{'#' * SEPARATOR_LENGTH} {module} start {'#' * SEPARATOR_LENGTH}"
        )

        if not os.path.isfile(module_file_path):
            raise FileNotFoundError(f"Module file not found: {module_file_path}")

        with open(module_file_path, "r", encoding="utf-8") as module_file:
            module_content = module_file.read()
            module_lines = module_content.splitlines()
            for module_line in module_lines:
                if module_line:
                    expand_result = self.expand_line(
                        module_line,
                        self.parser.calculate_indent_level(module_line) + space_indent,
                    )
                    if isinstance(expand_result, str):
                        # 展開された行を追加
                        expand_results.append(expand_result)
                    else:
                        # その他の行はそのまま表示
                        expand_results.append(f"{INDENT * space_indent}{module_line}")
                else:
                    expand_results.append("")
        expand_results.append("")
        expand_results.append(
            f"{INDENT * space_indent}{'#' * SEPARATOR_LENGTH} {module} end   {'#' * SEPARATOR_LENGTH}"
        )
        return "\n".join(expand_results)

    def expand_file(self, file_path: str) -> list[str]:
        """ファイルを読み込んでインポート文を展開する"""
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        expand_results = []
        lines = content.splitlines()
        for line in lines:
            expand_result = self.expand_line(line, 0)
            if expand_result is not None:
                expand_results.append(expand_result)
            else:
                expand_results.append(line)
        expand_results.append("")
        return expand_results


class ExpanderConfig:
    """展開ツールの設定を管理するクラス"""

    def __init__(self, file_path: str, expand_path: str):
        self.file_path = file_path
        self.expand_path = expand_path
        self.expand_folder = self._extract_folder_name(expand_path)

    @staticmethod
    def _extract_folder_name(expand_path: str) -> str:
        """展開対象のフォルダ名を取得する"""
        expand_path = os.path.abspath(expand_path)
        expand_folder = expand_path.split(os.sep)[-1]
        if expand_folder.endswith(".py"):
            expand_folder = expand_folder[:-3]
        return expand_folder

    @classmethod
    def from_command_line(cls) -> "ExpanderConfig":
        """コマンドライン引数から設定を作成する"""
        if len(sys.argv) < 2:
            raise ValueError("Usage: python expander.py <file_path> [expand_path]")

        file_path = sys.argv[1]
        # expand_pathが指定されていない場合は、expander.pyと同じディレクトリを使用
        expand_path = (
            sys.argv[2]
            if len(sys.argv) > 2
            else os.path.dirname(os.path.abspath(__file__))
        )

        if not file_path or not os.path.isfile(file_path):
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

        return cls(file_path, expand_path)


class ExpanderApplication:
    """展開ツールのメインアプリケーションクラス"""

    def __init__(self, config: ExpanderConfig):
        self.config = config
        self.expander = ModuleExpander(config.expand_folder)

    def run(self) -> None:
        """アプリケーションを実行する"""
        expand_results = self.expander.expand_file(self.config.file_path)
        output_content = "\n".join(expand_results)

        # 処理完了メッセージを標準エラー出力に表示
        print(f"展開完了: {self.config.file_path} -> 標準出力", file=sys.stderr)

        # 結果を標準出力に出力
        print(output_content)


def main() -> None:
    """ファイルにインポートされているライブラリを展開する"""
    app = ExpanderApplication(ExpanderConfig.from_command_line())
    app.run()


if __name__ == "__main__":
    main()
