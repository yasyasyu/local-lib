import os
import sys

SPACE = " "
INDENT_SIZE = 4
INDENT = SPACE * INDENT_SIZE

exist_import = set()


def current_indent(line: str) -> int:
    return (len(line) - len(line.lstrip())) // len(INDENT)


def expand_line(line: str, expand_folder, current_space_indent) -> str | None:

    if not (
        line.lstrip().startswith(f"from {expand_folder}")
        or line.lstrip().startswith(f"from .")
        or line.lstrip().startswith(f"import {expand_folder}")
    ):
        return None

    expand_results = []

    space_indent = current_indent(line)
    expand_results.append(
        f"{INDENT*(space_indent + current_space_indent)}# {line.lstrip()}"
    )

    line = line.lstrip()
    # インポート文を展開
    if line.startswith("from ."):
        # from .folder.filename import classname
        # from .folder import filename
        parts = line.split("import")
        module = parts[0].replace("from .", "").strip()
        if "." in module:
            # ネストされたモジュールの場合
            module_file_path = os.path.abspath(
                "./" + f"{expand_folder}" + "/".join(module.split(".")) + ".py"
            )
            module = f"{expand_folder}/".join(module.split("."))
            imported = parts[1].strip()

        else:
            # import モジュール
            module_file_path = os.path.abspath(
                "./" + expand_folder + "/" + module + ".py"
            )
            imported = parts[1].strip()
            module = f"{expand_folder}" + "/" + "/".join(module.split("."))

    elif line.startswith("from "):
        # from folder.filename import classname
        # from folder import filename
        parts = line.split("import")
        module = parts[0].replace("from ", "").strip()
        if "." in module:
            # ネストされたモジュールの場合
            module_file_path = os.path.abspath(
                "./" + "/".join(module.split(".")) + ".py"
            )
            module = "/".join(module.split("."))
            imported = parts[1].strip()

        else:
            raise NotImplementedError(
                "from folder.filename import classname の形式のみ実装済みです。"
            )
            # import モジュール
            module_file_path = os.path.abspath(
                "./" + module + "/" + parts[1].strip() + ".py"
            )
            module = module + "/" + parts[1].strip()
            imported = ""

    elif line.startswith("import "):
        raise NotImplementedError(
            "from folder.filename import classname の形式のみ実装済みです。"
        )
        # import モジュール
        module = line.replace("import ", "").strip()
        if "." in module:
            # ネストされたモジュールの場合
            module_file_path = os.path.abspath("./" + "/".join(module.split(".")))

        else:
            # 単一のモジュールの場合
            module = module.strip()

        print(f"{module=}")
    else:
        # ここには入らないはず
        raise ValueError(f"Unsupported import line: {line}")

    if module in exist_import:
        print(f"Skip module\t[{module}]", file=sys.stderr)
        return "\n".join(expand_results)
    exist_import.add(module)

    print(f"Expand module\t[{module}]", file=sys.stderr)
    expand_results.append(
        expand_imports(
            module_file_path, module, expand_folder, space_indent + current_space_indent
        )
    )
    return "\n".join(expand_results)


def expand_imports(module_file_path, module, expand_folder, space_indent) -> str:
    expand_results = []
    expand_results.append(
        f"{INDENT * space_indent}{'#'*INDENT_SIZE **2} {module} start {'#'*INDENT_SIZE**2}"
    )

    if not os.path.isfile(module_file_path):
        raise FileNotFoundError(f"Module file not found: {module_file_path}")

    with open(module_file_path, "r", encoding="utf-8") as module_file:
        module_content = module_file.read()
        module_lines = module_content.splitlines()
        for module_line in module_lines:
            if module_line:
                expand_result = expand_line(
                    module_line,
                    expand_folder,
                    current_indent(module_line) + space_indent,
                )
                if isinstance(expand_result, str):
                    # 展開された行を追加
                    expand_results.append(f"{expand_result}")
                else:
                    # その他の行はそのまま表示
                    expand_results.append(f"{INDENT*space_indent}{module_line}")
            else:
                expand_results.append("")
    expand_results.extend(["", ""])
    expand_results.append(
        f"{INDENT * space_indent}{'#'*INDENT_SIZE**2} {module} end {'#'*INDENT_SIZE**2}"
    )
    return "\n".join(expand_results)


def main():
    """ファイルにインポートされているライブラリを展開する"""

    # ファイルのパスを取得
    file_path = sys.argv[1]
    expand_path = sys.argv[2]
    expand_path = os.path.abspath(expand_path)
    expand_folder = expand_path.split(os.sep)[-1]
    if expand_folder.endswith(".py"):
        expand_folder = expand_folder[:-3]

    expand_results = []
    if not file_path or not os.path.isfile(file_path):
        raise ValueError("Usage: python expander.py <file_path>")

    # ファイルを読み込み、インポート文を展開
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # インポート文を展開する処理（ここでは単純な例として置換）
    lines = content.splitlines()
    for line in lines:
        expand_result = expand_line(line, expand_folder, 0)
        if isinstance(expand_result, str):
            # その他の行はそのまま表示
            expand_results.append(f"{expand_result}")
        else:
            expand_results.append(line)
    expand_results.append("")
    if len(sys.argv) > 3:
        # 追加の引数がある場合は、展開された内容をファイルに書き込む
        output_file = sys.argv[3]
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write("\n".join(expand_results))
        print(f"Expanded content written to {output_file}")
        return
    else:
        # 展開された内容を表示
        print("\n".join(expand_results))


if __name__ == "__main__":
    main()
