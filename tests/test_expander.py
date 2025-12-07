"""expander.pyのテストコード"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from expander import (
    ImportParser,
    ModuleExpander,
    ExpanderConfig,
    ExpanderApplication,
    ParsedImport,
)


class TestImportParser(unittest.TestCase):
    """ImportParserクラスのテスト"""

    def setUp(self):
        """テストの前処理"""
        self.parser = ImportParser("local_lib")

    def test_calculate_indent_level_no_indent(self):
        """インデントなしの場合"""
        self.assertEqual(
            self.parser.calculate_indent_level("from module import func"), 0
        )

    def test_calculate_indent_level_single_indent(self):
        """1つのインデント"""
        self.assertEqual(
            self.parser.calculate_indent_level("    from module import func"), 1
        )

    def test_calculate_indent_level_multiple_indents(self):
        """複数のインデント"""
        self.assertEqual(
            self.parser.calculate_indent_level("        from module import func"), 2
        )
        self.assertEqual(
            self.parser.calculate_indent_level("            from module import func"), 3
        )

    def test_should_expand_relative_import(self):
        """相対インポートは展開対象"""
        self.assertTrue(self.parser.should_expand("from .module import func"))

    def test_should_expand_folder_import(self):
        """指定フォルダのインポートは展開対象"""
        self.assertTrue(self.parser.should_expand("from local_lib.module import func"))

    def test_should_not_expand_other_import(self):
        """他のインポートは展開対象外"""
        self.assertFalse(self.parser.should_expand("from os import path"))
        self.assertFalse(self.parser.should_expand("import sys"))

    def test_parse_simple_relative_import(self):
        """シンプルな相対インポート"""
        result = self.parser.parse_relative_import("from .module import func")
        self.assertIsInstance(result, ParsedImport)
        self.assertEqual(result.module, "local_lib/module")
        # Windows/Linuxの両方に対応
        expected_path = os.path.join("local_lib", "module.py")
        self.assertTrue(
            result.module_file_path.endswith(expected_path.replace("/", os.sep))
        )

    def test_parse_nested_relative_import(self):
        """ネストされた相対インポート"""
        result = self.parser.parse_relative_import("from .sub.module import func")
        self.assertIsInstance(result, ParsedImport)
        self.assertEqual(result.module, "local_lib/sub/module")
        # Windows/Linuxの両方に対応
        expected_path = os.path.join("local_lib", "sub", "module.py")
        self.assertTrue(
            result.module_file_path.endswith(expected_path.replace("/", os.sep))
        )

    def test_parse_nested_absolute_import(self):
        """ネストされた絶対インポート"""
        result = self.parser.parse_absolute_import("from local_lib.module import func")
        self.assertIsInstance(result, ParsedImport)
        self.assertEqual(result.module, "local_lib/module")
        # Windows/Linuxの両方に対応
        expected_path = os.path.join("local_lib", "module.py")
        self.assertTrue(
            result.module_file_path.endswith(expected_path.replace("/", os.sep))
        )

    def test_parse_invalid_absolute_import(self):
        """無効な絶対インポート（ドットなし）"""
        with self.assertRaises(ValueError):
            self.parser.parse_absolute_import("from module import func")

    def test_parse_integration(self):
        """parse統合テスト"""
        result = self.parser.parse("from .module import func")
        self.assertIsInstance(result, ParsedImport)
        self.assertEqual(result.module, "local_lib/module")


class TestExpanderConfig(unittest.TestCase):
    """ExpanderConfigクラスのテスト"""

    def test_extract_folder_name(self):
        """フォルダパスの場合"""
        config = ExpanderConfig("test.py", "local_lib")
        self.assertEqual(config.expand_folder, "local_lib")

    def test_extract_folder_name_from_py_file(self):
        """.pyファイルパスの場合"""
        config = ExpanderConfig("test.py", "local_lib.py")
        self.assertEqual(config.expand_folder, "local_lib")


class TestModuleExpander(unittest.TestCase):
    """ModuleExpanderクラスのテスト（統合テスト）"""

    def setUp(self):
        """テストの前処理"""
        # テンポラリディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        self.test_lib_dir = os.path.join(self.temp_dir, "test_lib")
        os.makedirs(self.test_lib_dir)

        # テスト用のモジュールファイルを作成
        self.module_path = os.path.join(self.test_lib_dir, "test_module.py")
        with open(self.module_path, "w", encoding="utf-8") as f:
            f.write("def test_func():\n    pass\n")

        # ModuleExpanderインスタンスを作成
        self.expander = ModuleExpander("test_lib")

    def tearDown(self):
        """テストの後処理"""
        import shutil
        import time

        # カレントディレクトリを変更してファイルロックを解除
        os.chdir(os.path.dirname(__file__))
        time.sleep(0.1)  # ファイルが解放されるまで待機
        try:
            shutil.rmtree(self.temp_dir)
        except PermissionError:
            # Windows環境でのファイルロック問題を回避
            pass

    def test_expand_relative_import(self):
        """相対インポートの展開"""
        os.chdir(self.temp_dir)
        result = self.expander.expand_line("from .test_module import func", 0)
        self.assertIsNotNone(result)
        self.assertIn("# from .test_module import func", result)
        self.assertIn("test_lib/test_module start", result)
        self.assertIn("def test_func():", result)

    def test_non_expandable_line(self):
        """展開対象外の行"""
        result = self.expander.expand_line("import os", 0)
        self.assertIsNone(result)

    def test_duplicate_import(self):
        """重複したインポート"""
        os.chdir(self.temp_dir)
        # 1回目は展開される
        result1 = self.expander.expand_line("from .test_module import func", 0)
        self.assertIsNotNone(result1)
        self.assertIn("def test_func():", result1)

        # 2回目はスキップされる（モジュール内容は展開されない）
        result2 = self.expander.expand_line("from .test_module import func", 0)
        self.assertIsNotNone(result2)
        self.assertNotIn("def test_func():", result2)


def run_tests():
    """テストを実行"""
    unittest.main(argv=[""], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
