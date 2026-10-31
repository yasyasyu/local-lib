"""考察の振り返りノート（REVIEW_NOTES.md）に記録するスクリプト（ローカルで使う。提出用ではない）

使い方（``d:\\work`` で、``d:\\work\\review.ps1`` から実行する。``python local_lib/review.py ...`` でも同じ）::

    .\\review.ps1                       # 記録する（質問に答えるだけ）
    .\\review.ps1 add "ARC180 A" -i "操作で和の偶奇が変わらない" -t 3.3
    .\\review.ps1 due                   # 今日までに解き直す問題を表示
    .\\review.ps1 done "ARC180 A"       # 解き直した（解けなければ1週間後に延ばす）
    .\\review.ps1 stats                 # 型ごとの集計（苦手な型が分かる）

型が分からなければ空のまま記録する（「未分類」になる）。VS Code の Claude Code で /classify を実行すると、
AI が THINKING_GUIDE.md の型の定義と問題文を見て分類し、理由と一緒に書き込む
（中で unclassified と set-type を使う）。

記録すると、解き直す日（1週間後）が自動で入る。ノートは Markdown なので、手で直してもよい。
型の番号は THINKING_GUIDE.md の「3. 詰まったときに試すこと」と同じ。

https://github.com/yasyasyu/local-lib/blob/master/review.py
"""

import argparse
import datetime
import re
from dataclasses import dataclass
from pathlib import Path

NOTES = Path(__file__).with_name("REVIEW_NOTES.md")
INTERVAL = datetime.timedelta(days=7)  # 解き直すまでの間隔
TYPES = {
    "3.1": "言い換え",
    "3.2": "必要条件",
    "3.3": "不変量・偶奇",
    "3.4": "逆から",
    "3.5": "上限・下限",
    "3.6": "1つ固定",
    "3.7": "寄与",
    "3.8": "極端な場合",
}
HEADER = (
    "# 振り返りノート\n\n"
    "`d:\\work` で `.\\review.ps1` を実行して追記する（手で直してもよい）。"
    "書き方と型の番号は [THINKING_GUIDE.md](THINKING_GUIDE.md) を参照。\n"
)


@dataclass
class Entry:
    """ノートの1問分"""

    problem: str
    date: str  # 記録した日（YYYY-MM-DD）
    idea: str  # 必要だった発想
    types: list[str]  # 型の番号（"3.3" など）
    memo: str
    due: str  # 解き直す日（YYYY-MM-DD）
    done: bool  # 解き直して解けたか


def normalize(problem: str) -> str:
    """問題名を比べるための形にする（空白・"-"・"_" を除いて大文字に）。O(len(problem))"""
    return re.sub(r"[\s_\-]", "", problem).upper()


def parse_types(s: str) -> list[str] | None:
    """「3.3 3.1」「3, 1」のような入力を型の番号のリストにする。不正なら None。O(len(s))"""
    res = []
    for t in re.split(r"[\s,、]+", s.strip()):
        if not t:
            continue
        if t.isdigit():
            t = "3." + t
        if t not in TYPES:
            return None
        if t not in res:
            res.append(t)
    return res


def format_types(types: list[str]) -> str:
    """型の番号のリストを「3.3 不変量・偶奇, 3.1 言い換え」の形にする。空なら「未分類」。O(len(types))"""
    return ", ".join(f"{t} {TYPES.get(t, '')}".strip() for t in types) or "未分類"


def format_entry(e: Entry) -> str:
    """1問分を Markdown にする。O(1)"""
    return (
        f"### {e.problem}\n"
        f"- 日付: {e.date}\n"
        f"- 必要だった発想: {e.idea}\n"
        f"- 型: {format_types(e.types)}\n"
        f"- メモ: {e.memo}\n"
        f"- 解き直し: {e.due} {'済' if e.done else '未'}\n"
    )


def parse_notes(text: str) -> list[Entry]:
    """ノートの Markdown から、1問ずつ取り出す。項目が欠けていても読める。O(len(text))"""
    entries = []
    fields: dict[str, str] | None = None
    title = ""

    def flush() -> None:
        if fields is None:
            return
        m = re.search(r"(\d{4}-\d{2}-\d{2})\s*(未|済)?", fields.get("解き直し", ""))
        entries.append(
            Entry(
                problem=title,
                date=fields.get("日付", ""),
                idea=fields.get("必要だった発想", ""),
                types=re.findall(r"3\.\d", fields.get("型", "")),
                memo=fields.get("メモ", ""),
                due=m.group(1) if m else "",
                done=bool(m and m.group(2) == "済"),
            )
        )

    for line in text.splitlines():
        if line.startswith("### "):
            flush()
            title = line[4:].strip()
            fields = {}
        elif fields is not None:
            m = re.match(r"-\s*([^:：]+)[:：]\s*(.*)$", line)
            if m:
                fields[m.group(1).strip()] = m.group(2).strip()
    flush()
    return entries


def read_notes(path: Path) -> list[Entry]:
    """ノートのファイルを読む（無ければ空）。O(ファイルの大きさ)"""
    if not path.exists():
        return []
    return parse_notes(path.read_bytes().decode("utf-8"))


def add_entry(path: Path, e: Entry) -> None:
    """ノートの末尾に1問分を追記する（ファイルが無ければ作る）。O(ファイルの大きさ)"""
    text = path.read_bytes().decode("utf-8") if path.exists() else HEADER
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + format_entry(e)
    path.write_bytes(text.encode("utf-8"))  # Windows でも改行を LF のままにする


def _set_field(path: Path, problem: str, key: str, value: str, after: str | None = None) -> bool:
    """problem の記録（複数あれば最後のもの）の「- key: ...」の行だけを書き換える。O(ファイルの大きさ)

    手で書き足した部分を消さないように、他の行はそのまま残す。
    行が無ければ、「- after: ...」の行の次（after が無いか見つからなければ、その問題の最後）に足す。
    記録が見つからなければ False。
    """
    if not path.exists():
        return False
    lines = path.read_bytes().decode("utf-8").split("\n")
    target = -1
    for i, line in enumerate(lines):
        if line.startswith("### ") and normalize(line[4:]) == normalize(problem):
            target = i
    if target == -1:
        return False
    end = target + 1
    while end < len(lines) and not lines[end].startswith("### "):
        end += 1

    def find(k: str) -> int:
        for i in range(target + 1, end):
            if re.match(rf"-\s*{re.escape(k)}\s*[:：]", lines[i]):
                return i
        return -1

    new_line = f"- {key}: {value}"
    i = find(key)
    if i != -1:
        lines[i] = new_line
    else:
        k = find(after) if after is not None else -1
        if k != -1:
            j = k + 1
        else:
            # その問題の最後（後ろの空行の手前）
            j = end
            while j > target + 1 and lines[j - 1] == "":
                j -= 1
        lines.insert(j, new_line)
    path.write_bytes("\n".join(lines).encode("utf-8"))
    return True


def set_due(path: Path, problem: str, due: str, done: bool) -> bool:
    """problem の記録の「解き直し」の行を書き換える。見つからなければ False。O(ファイルの大きさ)"""
    return _set_field(path, problem, "解き直し", f"{due} {'済' if done else '未'}")


def set_types(path: Path, problem: str, types: list[str], reason: str) -> bool:
    """problem の記録の「型」を書き換え、そのすぐ下に「分類の理由（AI）」を書く。O(ファイルの大きさ)

    /classify（Claude Code のコマンド）から使う。見つからなければ False。
    """
    if not _set_field(path, problem, "型", format_types(types)):
        return False
    return _set_field(path, problem, "分類の理由（AI）", reason, after="型")


def due_entries(entries: list[Entry], today: str) -> list[Entry]:
    """解き直す日が today 以前で、まだ解けていない問題を、解き直す日の順に返す。O(K log K)"""
    res = [e for e in entries if e.due and not e.done and e.due <= today]
    return sorted(res, key=lambda e: e.due)


def type_counts(entries: list[Entry]) -> list[tuple[str, int]]:
    """型ごとの問題数を、多い順に返す。O(K)"""
    cnt: dict[str, int] = {}
    for e in entries:
        for t in e.types:
            cnt[t] = cnt.get(t, 0) + 1
    return sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))


def _ask(prompt: str, allow_empty: bool = False) -> str:
    """空でない答えが返るまで聞く（allow_empty なら空でもよい）"""
    while True:
        s = input(prompt).strip()
        if s or allow_empty:
            return s


def _ask_types() -> list[str]:
    """型の番号を聞く。番号の一覧を見せて、正しい入力が来るまで聞き直す"""
    keys = list(TYPES)
    for i in range(0, len(keys), 4):
        print("  " + "   ".join(f"{k} {TYPES[k]}" for k in keys[i : i + 4]))
    while True:
        types = parse_types(input("型（番号。複数なら空白区切り。分からなければ空）: "))
        if types is not None:
            return types
        print("  3.1〜3.8（または 1〜8）で入力してください")


def main(
    argv: list[str] | None = None, path: Path = NOTES, today: datetime.date | None = None
) -> None:
    """コマンドラインの入口。O(ファイルの大きさ)"""
    today = today or datetime.date.today()
    parser = argparse.ArgumentParser(description="考察の振り返りノートに記録する")
    sub = parser.add_subparsers(dest="cmd")
    p_add = sub.add_parser("add", help="記録する（省略した項目は質問する）")
    p_add.add_argument("problem", nargs="?", help='問題（例: "ARC180 A"）')
    p_add.add_argument("-i", "--idea", help="必要だった発想")
    p_add.add_argument("-t", "--types", help='型の番号（例: "3.3 3.1"）')
    p_add.add_argument("-m", "--memo", help="メモ")
    sub.add_parser("due", help="今日までに解き直す問題を表示する")
    p_done = sub.add_parser("done", help="解き直した結果を記録する")
    p_done.add_argument("problem", help='問題（例: "ARC180 A"）')
    g = p_done.add_mutually_exclusive_group()
    g.add_argument("-y", "--solved", action="store_true", help="解けた")
    g.add_argument("-n", "--failed", action="store_true", help="解けなかった（1週間後に延ばす）")
    sub.add_parser("stats", help="型ごとの集計を表示する")
    sub.add_parser("unclassified", help="型が未分類の問題を表示する（/classify から使う）")
    p_set = sub.add_parser("set-type", help="型と分類の理由を書き込む（/classify から使う）")
    p_set.add_argument("problem", help='問題（例: "ARC180 A"）')
    p_set.add_argument("-t", "--types", required=True, help='型の番号（例: "3.3 3.1"）')
    p_set.add_argument("-r", "--reason", required=True, help="分類の理由")
    args = parser.parse_args(argv)

    if args.cmd in (None, "add"):
        problem = (getattr(args, "problem", None) or _ask("問題（例: ARC180 A）: ")).strip()
        if any(normalize(e.problem) == normalize(problem) for e in read_notes(path)):
            print("  （同じ問題の記録がすでにあります。新しい記録として追記します）")
        idea = getattr(args, "idea", None) or _ask("必要だった発想: ")
        if getattr(args, "types", None) is not None:
            types = parse_types(args.types)
            if types is None:
                parser.error("型は 3.1〜3.8（または 1〜8）で指定してください")
        else:
            types = _ask_types()
        memo = getattr(args, "memo", None)
        if memo is None:
            memo = _ask("メモ（空でよい）: ", allow_empty=True)
        due = (today + INTERVAL).isoformat()
        add_entry(path, Entry(problem, today.isoformat(), idea, types, memo, due, False))
        print(f"→ {path.name} に追記しました（解き直し: {due}）")
        if not types:
            print("  型は未分類です。VS Code の Claude Code で /classify を実行すると、AI が分類します")

    elif args.cmd == "due":
        entries = due_entries(read_notes(path), today.isoformat())
        if not entries:
            print("今日までに解き直す問題はありません")
        for e in entries:
            print(f"{e.due}  {e.problem}  （{e.idea}）")

    elif args.cmd == "done":
        if args.solved or args.failed:
            solved = args.solved
        else:
            solved = _ask("解けましたか？ [y/n]: ").lower().startswith("y")
        due = today.isoformat() if solved else (today + INTERVAL).isoformat()
        if not set_due(path, args.problem, due, solved):
            print(f"{args.problem} の記録が見つかりません")
        elif solved:
            print(f"{args.problem}: 解き直し済みにしました")
        else:
            print(f"{args.problem}: 解き直しを {due} に延ばしました")

    elif args.cmd == "stats":
        entries = read_notes(path)
        done = sum(e.done for e in entries)
        due = len(due_entries(entries, today.isoformat()))
        print(f"記録 {len(entries)} 問（解き直し済み {done}、今日までに解き直す問題 {due}）")
        counts = type_counts(entries)
        if counts:
            width = max(len(TYPES.get(t, "")) for t, _ in counts)
            for t, c in counts:
                name = TYPES.get(t, "")
                pad = "　" * (width - len(name))  # 名前は全角なので、全角空白で揃える
                print(f"  {t} {name}{pad} {'■' * c} {c}")
        unclassified = sum(not e.types for e in entries)
        if unclassified:
            print(f"未分類 {unclassified} 問（VS Code の Claude Code で /classify を実行すると分類します）")

    elif args.cmd == "unclassified":
        entries = [e for e in read_notes(path) if not e.types]
        if not entries:
            print("未分類の問題はありません")
        for e in entries:
            print(f"### {e.problem}")
            print(f"- 必要だった発想: {e.idea}")
            print(f"- メモ: {e.memo}")

    elif args.cmd == "set-type":
        types = parse_types(args.types)
        if not types:
            parser.error("型は 3.1〜3.8（または 1〜8）で1つ以上指定してください")
        if set_types(path, args.problem, types, args.reason):
            print(f"{args.problem}: 型を {format_types(types)} にしました")
        else:
            print(f"{args.problem} の記録が見つかりません")


if __name__ == "__main__":
    main()
