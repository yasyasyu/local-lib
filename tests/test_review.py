"""review.pyのテストコード"""

import datetime
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent))

from review import (
    Entry,
    add_entry,
    due_entries,
    format_entry,
    main,
    normalize,
    parse_notes,
    parse_types,
    set_due,
    set_types,
    type_counts,
)

TODAY = datetime.date(2026, 10, 25)


class TestHelpers(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("arc180 a"), normalize("ARC180A"))
        self.assertEqual(normalize("ABC-300_F"), "ABC300F")

    def test_parse_types(self):
        self.assertEqual(parse_types("3.3 3.1"), ["3.3", "3.1"])
        self.assertEqual(parse_types("3, 1、3"), ["3.3", "3.1"])
        self.assertEqual(parse_types(""), [])
        self.assertIsNone(parse_types("3.9"))
        self.assertIsNone(parse_types("abc"))

    def test_format_and_parse_round_trip(self):
        e = Entry("ARC180 A", "2026-10-25", "和の偶奇が変わらない", ["3.3", "3.1"], "N=1 を忘れた", "2026-11-01", False)
        text = format_entry(e)
        self.assertIn("- 型: 3.3 不変量・偶奇, 3.1 言い換え", text)
        self.assertEqual(parse_notes(text), [e])

    def test_parse_hand_written_notes(self):
        text = "# メモ\n\n### ABC300 F\n- 必要だった発想：寄与で数える\n自由に書いた行\n- 型: 3.7\n\n### X\n"
        entries = parse_notes(text)
        self.assertEqual([e.problem for e in entries], ["ABC300 F", "X"])
        self.assertEqual(entries[0].idea, "寄与で数える")
        self.assertEqual(entries[0].types, ["3.7"])
        self.assertEqual(entries[0].due, "")
        self.assertFalse(entries[0].done)

    def test_due_and_counts(self):
        es = [
            Entry("A", "", "", ["3.3"], "", "2026-10-20", False),
            Entry("B", "", "", ["3.3", "3.1"], "", "2026-10-30", False),
            Entry("C", "", "", ["3.1"], "", "2026-10-01", True),
            Entry("D", "", "", [], "", "2026-10-24", False),
        ]
        self.assertEqual([e.problem for e in due_entries(es, "2026-10-25")], ["A", "D"])
        self.assertEqual(type_counts(es), [("3.1", 2), ("3.3", 2)])


class TestFile(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "REVIEW_NOTES.md"

    def tearDown(self):
        self.dir.cleanup()

    def run_main(self, argv, inputs=()):
        buf = io.StringIO()
        with mock.patch("builtins.input", side_effect=list(inputs)), redirect_stdout(buf):
            main(argv, self.path, TODAY)
        return buf.getvalue()

    def test_add_with_arguments_creates_file(self):
        out = self.run_main(["add", "ARC180 A", "-i", "和の偶奇", "-t", "3.3", "-m", ""])
        self.assertIn("2026-11-01", out)
        text = self.path.read_bytes().decode("utf-8")
        self.assertTrue(text.startswith("# 振り返りノート"))
        self.assertNotIn("\r", text)
        [e] = parse_notes(text)
        self.assertEqual((e.problem, e.idea, e.types, e.date, e.due, e.done), ("ARC180 A", "和の偶奇", ["3.3"], "2026-10-25", "2026-11-01", False))

    def test_interactive_add_reasks_invalid_types(self):
        self.run_main([], ["ARC181 A", "", "逆から見る", "9", "3.4 6", "メモ"])
        [e] = parse_notes(self.path.read_bytes().decode("utf-8"))
        self.assertEqual((e.problem, e.idea, e.types, e.memo), ("ARC181 A", "逆から見る", ["3.4", "3.6"], "メモ"))

    def test_done_keeps_hand_written_lines(self):
        self.run_main(["add", "ARC180 A", "-i", "x", "-t", "3.3", "-m", ""])
        self.run_main(["add", "ARC181 A", "-i", "y", "-t", "3.1", "-m", ""])
        text = self.path.read_bytes().decode("utf-8").replace("- メモ: \n", "- メモ: \n手で書いた考察\n", 1)
        self.path.write_bytes(text.encode("utf-8"))

        out = self.run_main(["done", "arc180a"], ["n"])
        self.assertIn("2026-11-01", out)
        out = self.run_main(["done", "ARC181 A", "-y"])
        self.assertIn("済み", out)
        text = self.path.read_bytes().decode("utf-8")
        self.assertIn("手で書いた考察", text)
        a, b = parse_notes(text)
        self.assertEqual((a.due, a.done), ("2026-11-01", False))
        self.assertEqual((b.due, b.done), ("2026-10-25", True))

    def test_done_adds_missing_due_line(self):
        self.path.write_bytes("### ABC300 F\n- 型: 3.7\n\n### X\n".encode("utf-8"))
        self.assertTrue(set_due(self.path, "ABC300 F", "2026-10-25", True))
        [a, x] = parse_notes(self.path.read_bytes().decode("utf-8"))
        self.assertEqual((a.due, a.done, a.types), ("2026-10-25", True, ["3.7"]))
        self.assertEqual(x.due, "")

    def test_done_unknown_problem(self):
        self.run_main(["add", "ARC180 A", "-i", "x", "-t", "", "-m", ""])
        out = self.run_main(["done", "ARC999 A", "-y"])
        self.assertIn("見つかりません", out)

    def test_due_and_stats_output(self):
        add_entry(self.path, Entry("A", "2026-10-10", "x", ["3.3"], "", "2026-10-17", False))
        add_entry(self.path, Entry("B", "2026-10-20", "y", ["3.3", "3.7"], "", "2026-10-27", False))
        out = self.run_main(["due"])
        self.assertIn("A", out)
        self.assertNotIn("B", out)
        out = self.run_main(["stats"])
        self.assertIn("記録 2 問", out)
        self.assertIn("3.3 不変量・偶奇 ■■ 2", out)
        self.assertIn("3.7 寄与", out)

    def test_due_empty(self):
        self.assertIn("ありません", self.run_main(["due"]))

    def test_empty_types_is_unclassified(self):
        out = self.run_main(["add", "ARC180 A", "-i", "x", "-t", "", "-m", ""])
        self.assertIn("/classify", out)
        text = self.path.read_bytes().decode("utf-8")
        self.assertIn("- 型: 未分類", text)
        self.assertEqual(parse_notes(text)[0].types, [])
        self.assertIn("未分類 1 問", self.run_main(["stats"]))

    def test_unclassified_lists_only_unclassified(self):
        self.run_main(["add", "ARC180 A", "-i", "和の偶奇", "-t", "", "-m", "N=1"])
        self.run_main(["add", "ARC181 A", "-i", "逆から", "-t", "3.4", "-m", ""])
        out = self.run_main(["unclassified"])
        self.assertIn("### ARC180 A", out)
        self.assertIn("- 必要だった発想: 和の偶奇", out)
        self.assertNotIn("ARC181 A", out)

    def test_set_type_keeps_other_lines(self):
        self.run_main(["add", "ARC180 A", "-i", "和の偶奇", "-t", "", "-m", "N=1"])
        self.run_main(["add", "ARC181 A", "-i", "y", "-t", "", "-m", ""])
        text = self.path.read_bytes().decode("utf-8").replace("- メモ: N=1\n", "- メモ: N=1\n手で書いた考察\n")
        self.path.write_bytes(text.encode("utf-8"))

        out = self.run_main(["set-type", "arc180a", "-t", "3.3", "-r", "操作で和の偶奇が変わらないため"])
        self.assertIn("3.3 不変量・偶奇", out)
        text = self.path.read_bytes().decode("utf-8")
        self.assertIn("手で書いた考察", text)
        self.assertIn("- 型: 3.3 不変量・偶奇\n- 分類の理由（AI）: 操作で和の偶奇が変わらないため\n", text)
        a, b = parse_notes(text)
        self.assertEqual(a.types, ["3.3"])
        self.assertEqual(b.types, [])

        # 分類し直すと、理由の行は増えずに書き換わる
        self.run_main(["set-type", "ARC180 A", "-t", "3.3 3.2", "-r", "必要条件でもある"])
        text = self.path.read_bytes().decode("utf-8")
        self.assertEqual(text.count("分類の理由"), 1)
        self.assertEqual(parse_notes(text)[0].types, ["3.3", "3.2"])

    def test_set_type_without_type_line(self):
        self.path.write_bytes("### X\n- 必要だった発想: z\n".encode("utf-8"))
        self.assertTrue(set_types(self.path, "X", ["3.7"], "寄与"))
        text = self.path.read_bytes().decode("utf-8")
        self.assertEqual(text, "### X\n- 必要だった発想: z\n- 型: 3.7 寄与\n- 分類の理由（AI）: 寄与\n")
        self.assertFalse(set_types(self.path, "Y", ["3.7"], "寄与"))

    def test_set_type_rejects_invalid(self):
        self.run_main(["add", "ARC180 A", "-i", "x", "-t", "", "-m", ""])
        with self.assertRaises(SystemExit), redirect_stdout(io.StringIO()), mock.patch("sys.stderr", io.StringIO()):
            main(["set-type", "ARC180 A", "-t", "9", "-r", "x"], self.path, TODAY)


if __name__ == "__main__":
    unittest.main()
