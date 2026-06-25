#!/usr/bin/env python3
"""Git diff review helper.

Generates a lightweight diff summary for self-review.

Usage:
  python scripts/diff_review_helper.py /path/to/project
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    """Run a command and return (exit_code, combined_output)."""
    try:
        out = subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.STDOUT)
        return 0, out
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.CalledProcessError as exc:
        return exc.returncode, exc.output


def git_output(args: list[str], cwd: Path) -> str:
    """Run a git command after repository validation."""
    code, out = run(["git", *args], cwd)
    # For diff --check, non-zero may mean whitespace/conflict problems; keep output.
    if code in (0, 1):
        return out
    return out


def is_git_repo(root: Path) -> tuple[bool, str]:
    code, out = run(["git", "rev-parse", "--is-inside-work-tree"], root)
    if code == 127:
        return False, "未找到 git 命令，请先安装 Git，或在带 Git 的环境中运行。"
    if code != 0 or out.strip().lower() != "true":
        return False, "当前目录不是 Git 仓库，无法检查 diff。请在项目根目录运行，或先执行 git init。"
    return True, ""


def status_files(status: str) -> list[str]:
    files = []
    for line in status.splitlines():
        if not line.strip():
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path.strip().strip('"'))
    return files


def risky_path(path: str) -> bool:
    risky_fragments = [
        ".env",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        "dist/",
        "build/",
        "__MACOSX",
        ".DS_Store",
        "/._",
    ]
    return any(fragment in path for fragment in risky_fragments) or Path(path).name.startswith("._")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize git diff, changed files, risky paths, and whitespace/conflict checks for self-review.",
        epilog="Example: python scripts/diff_review_helper.py /path/to/project",
    )
    parser.add_argument("project", nargs="?", default=".", help="Git project directory, defaults to current directory")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()

    print("# Diff Review Summary")
    print(f"Project: {root}")
    print()

    if not root.exists() or not root.is_dir():
        print("## Error")
        print(f"- 项目路径不存在或不是目录：`{root}`")
        return 2

    ok, message = is_git_repo(root)
    if not ok:
        print("## Error")
        print(f"- {message}")
        print()
        print("## Next Step")
        print("- 如果只是想做通用项目体检，可以改用：`python scripts/project_audit.py /path/to/project`")
        return 2

    status = git_output(["status", "--short"], root)
    stat = git_output(["diff", "--stat"], root)
    name_only = git_output(["diff", "--name-only"], root)
    staged_stat = git_output(["diff", "--cached", "--stat"], root)
    staged_name = git_output(["diff", "--cached", "--name-only"], root)
    diff_check = git_output(["diff", "--check"], root)
    staged_diff_check = git_output(["diff", "--cached", "--check"], root)

    print("## Git Status")
    print("```text")
    print(status.strip() or "clean")
    print("```")
    print()

    print("## Unstaged Diff Stat")
    print("```text")
    print(stat.strip() or "no unstaged diff")
    print("```")
    print()

    print("## Staged Diff Stat")
    print("```text")
    print(staged_stat.strip() or "no staged diff")
    print("```")
    print()

    files = [x.strip() for x in (name_only + "\n" + staged_name).splitlines() if x.strip()]
    files.extend(status_files(status))
    unique_files = sorted(set(files))

    print("## Changed Files")
    if unique_files:
        for f in unique_files:
            print(f"- `{f}`")
    else:
        print("- 无改动文件。")
    print()

    print("## Whitespace / Conflict Checks")
    check_output = "\n".join(x.strip() for x in [diff_check, staged_diff_check] if x.strip())
    if check_output:
        print("```text")
        print(check_output)
        print("```")
    else:
        print("- git diff --check 未发现空白或冲突标记问题。")
    print()

    risky = [f for f in unique_files if risky_path(f)]
    print("## Risk Hints")
    if risky:
        for f in risky:
            print(f"- 可能不应提交：`{f}`")
        print("建议修改后再提交。")
        return 1

    if check_output:
        print("- diff check 发现空白或冲突标记问题，建议修复后再提交。")
        return 1

    if unique_files:
        print("- 未发现明显不应提交的路径，但仍需人工检查密钥、本机路径、临时代码。")
        print("- 建议根据 SKILL.md 的 Diff 自查模板补充 MR 描述。")
    else:
        print("- 当前没有 diff。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
